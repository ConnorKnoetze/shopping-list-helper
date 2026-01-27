document.addEventListener("DOMContentLoaded", function() {
    //sidebar section
    const recipeSidebar = document.querySelector(".recipe-sidebar")
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;
    let currentScroll = window.scrollY;
    let maxScroll = document.documentElement.scrollHeight - windowHeight;

    const breakpoint = 850; // Define the breakpoint for mobile vs desktop

    function attachSidebarButton(button){
        button.innerHTML = `
        <svg width="24" height="24" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
        </svg>`;
        recipeSidebar.innerHTML += `
        <button class="close-sidebar-button" aria-label="Close Sidebar">
            <svg width="24" height="24" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
        </button>`;
    }

    if (windowWidth <= breakpoint && recipeSidebar) {
        const sidebarToggleButton = document.querySelector(".sidebar-toggle-button.hidden");
        sidebarToggleButton.classList.toggle("hidden")
        attachSidebarButton(sidebarToggleButton)
        const closeSidebarButton = document.querySelector(".close-sidebar-button");

        closeSidebarButton.addEventListener("click", function () {
            sidebarToggleButton.click();
        });

        // saved scroll position used when locking document scroll
        let _savedScrollY = 0;

        sidebarToggleButton.addEventListener("click", function () {
            const recipeDetail = document.querySelector(".recipe-detail-container");

            // toggle blurred state and capture the resulting state
            const isNowBlurred = recipeDetail.classList.toggle("blurred");
            recipeSidebar.classList.toggle("hidden");

            // If we opened the sidebar (blurred), lock the document scroll and preserve position
            if (isNowBlurred) {
                _savedScrollY = window.scrollY || window.pageYOffset || 0;
                // fix the body in place to prevent jump and preserve layout
                document.body.style.top = `-${_savedScrollY}px`;
                document.body.classList.add('scroll-locked');
            } else {
                // restore body and scroll position
                document.body.classList.remove('scroll-locked');
                // clear inline top so document can flow normally
                document.body.style.top = '';
                window.scrollTo(0, _savedScrollY);
            }
        });
        recipeSidebar.classList.toggle("hidden");
    }

    if (windowWidth > breakpoint && recipeSidebar) {
        window.addEventListener("scroll", function () {
            currentScroll = window.scrollY - 1;
            maxScroll = document.documentElement.scrollHeight - window.innerHeight;
            if (recipeSidebar) {
                // Calculate the scroll progress and adjust the sidebar position (120px is an offset for the sidebar height which tends to increase the height of the document)
                let scrollProgress = (currentScroll / (maxScroll + 1)) * (document.body.scrollHeight - recipeSidebar.scrollHeight - 140);
                recipeSidebar.style.transform = `translateY(${Math.trunc(scrollProgress)}px)`;
            }
        });
    }


    //Submit ingredient selection form
    // fixed selector: select the button with both classes
    const ingredientSubmitButton = document.querySelector(".btn.btn-primary");

    if (ingredientSubmitButton) {
        ingredientSubmitButton.addEventListener("click", function (e) {
            e.preventDefault();

            // collect checked checkboxes
            const checkedBoxes = Array.from(document.querySelectorAll(".ingredient-check:checked"));
            if (checkedBoxes.length === 0) {
                return; // nothing to submit
            }

            // build the ingredients strings from the DOM (name and qty)
            const ingredients = checkedBoxes.map(cb => {
                const li = cb.closest("li");
                const nameEl = li.querySelector(".ingredient-name");
                const name = nameEl ? nameEl.textContent.trim() : "";
                const qtyEl = li.querySelector(".ingredient-qty");
                const qty = qtyEl ? qtyEl.textContent.trim() : "";
                const unitEl = li.querySelector(".ingredient-unit");
                const unit = unitEl ? unitEl.textContent.trim() : "";

                return `${qty};;${unit};;${name}`;
            });

            // create a form and hidden inputs for ingredients[] then submit
            const form = document.createElement("form");
            form.method = "POST";
            form.action = ingredientSubmitButton.datasetAction || window.location.href;

            ingredients.forEach(value => {
                const input = document.createElement("input");
                input.type = "hidden";
                input.name = "ingredients[]";
                input.value = value;
                form.appendChild(input);
            });

            // attach and submit
            document.body.appendChild(form);
            form.submit();
        });
    }

    //Clear all ingredient selections
    const ingredientClearButton = document.getElementById('clear-all-ingredients');
    if (ingredientClearButton) {
        ingredientClearButton.addEventListener("click", function (e) {
            e.preventDefault();

            // visually uncheck all boxes
            const checkedBoxes = document.querySelectorAll(".ingredient-check:checked");

            // collect checked checkboxes
            if (checkedBoxes.length === 0) {
                return; // nothing to submit
            }

            checkedBoxes.forEach(cb => cb.checked = false);

            // submit an empty POST to clear persisted selections server-side
            const form = document.createElement('form');
            form.method = 'POST';
            // prefer explicit dataset action, fall back to the existing ingredients form action or current URL
            const parentForm = document.getElementById('ingredients-form');
            form.action = ingredientClearButton.datasetAction || (parentForm ? parentForm.action : window.location.href);

            document.body.appendChild(form);
            form.submit();
        });
    }

    //back button section
    const backButton = document.querySelector(".back-button");
    if (backButton) {
        backButton.addEventListener("click", function () {
            window.location.href = '/recipes';
        });
    }

    //toggle recipe save button
    const saveButton = document.querySelector(".save-recipe-button");
    if (saveButton) {
        saveButton.addEventListener("click", function () {
            // read recipe name from data attribute and URL-encode it for safe inclusion in path
            const rawName = saveButton.dataset ? saveButton.dataset.recipeName : saveButton.getAttribute('data-recipe-name');
            if (!rawName) {
                console.error('Save button missing data-recipe-name');
                return;
            }
            const recipeName = encodeURIComponent(rawName);

            // prepare headers; include CSRF token header if available
            const headers = {
                'Content-Type': 'application/json'
            };
            const csrfMeta = document.querySelector('meta[name="csrf-token"]');
            if (csrfMeta) {
                headers['X-CSRF-Token'] = csrfMeta.getAttribute('content') || '';
            }

            fetch(`/recipes/toggle_save/${recipeName}`, {
                method: 'POST',
                headers: headers,
            })
            .then(response => response.json())
            .then(data => {
                if (data.saved) {
                    saveButton.classList.add("saved");
                    saveButton.innerText = "Unsave";
                } else {
                    saveButton.classList.remove("saved");
                    saveButton.innerText = "Save Recipe";
                    window.location.href = `/recipes/${data.recipe_name}`;
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});