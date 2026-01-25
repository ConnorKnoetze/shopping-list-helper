document.addEventListener('DOMContentLoaded', function() {
    // Get all inventory cards
    const inventoryCards = document.querySelectorAll('.inventory-card');
    const ingredientPage = document.querySelector('.ingredient-page-container');
    const ingredientCloseButton = document.querySelector('.close-ingredient-page-button');


    function attachInnerHTML(data){
        if (ingredientPage) {
            ingredientPage.innerHTML = `
                <div class="ingredient-page-backdrop"></div>
                <div class="ingredient-page-content">
                    <button class="close-ingredient-page-button" aria-label="Close ingredient details">
                        <svg width="24" height="24" viewBox="0 0 24 24" 
                             stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="18" y1="6" x2="6" y2="18"/>
                            <line x1="6" y1="6" x2="18" y2="18"/>
                        </svg>
                    </button>
                    <div class="ingredient-page-inner-content">
                        <h2 class="ingredient-page-name">${data.name}</h2>
                        <p class="ingredient-page-category">Categories: <span>${data.categories || 'N/A'}</span></p>
                        <form class="ingredient-page-quantity-form" method="POST" action="/inventory/update/${data.name}">
                            <label for="quantity"></label>
                            <input type="range" id="quantity" name="quantity" value="${data.quantity || 0}" min="${data.range_min}" max="${data.range_max}" step="${data.step}" required />
                            <span id="quantity-value">${data.quantity || 0} ${data.unit || ''}</span>
                            <button type="submit" class="update-quantity-button">Add To List</button>
                        </form>
                    </div>
                </div>`;

            ingredientPage.classList.remove('hidden');
            document.body.classList.add('modal-open');

            // Attach dynamic listeners after render
            const newCloseButton = ingredientPage.querySelector('.close-ingredient-page-button');
            const backdrop = ingredientPage.querySelector('.ingredient-page-backdrop');
            const quantityInput = ingredientPage.querySelector('#quantity');
            const quantityValue = ingredientPage.querySelector('#quantity-value');

            // Update display on input/change
            if (quantityInput && quantityValue) {
                // Compute percent between min and max for the current value
                const getPercent = (val) => {
                    const min = parseFloat(quantityInput.min) || 0;
                    const max = parseFloat(quantityInput.max) || 100;
                    const value = parseFloat(val) || 0;
                    if (max === min) return 0;
                    return ((value - min) / (max - min)) * 100;
                };

                // Set the inline background so the filled portion matches the thumb
                const updateTrack = (val) => {
                    const pct = getPercent(val);
                    // set CSS variable used by the stylesheet
                    quantityInput.style.setProperty('--pct', pct + '%');
                };

                const updateDisplay = (val) => {
                    updateTrack(val);
                    quantityValue.textContent = `${val} ${data.unit || ''}`;
                };

                // initialize visuals
                updateDisplay(quantityInput.value);

                quantityInput.addEventListener('input', (e) => updateDisplay(e.target.value));
                quantityInput.addEventListener('change', (e) => updateDisplay(e.target.value));
            }

            // Handle form submission for quantity update
            const quantityForm = ingredientPage.querySelector('.ingredient-page-quantity-form');
            if (quantityForm) {
                quantityForm.addEventListener('submit', (e) => {
                    e.preventDefault();

                    const quantity = quantityInput.value;
                    const itemName = data.name;
                    const payload = {
                        quantity: quantity,
                        unit: data.unit
                    };

                    console.log('Sending payload:', payload);

                    fetch(`/inventory/update/${itemName}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'
                        },
                        body: JSON.stringify(payload)
                    })
                    .then(res => {
                        console.log('Response status:', res.status);
                        return res.json();
                    })
                    .then(response => {
                        console.log('Server response:', response);

                        // Handle success response
                        if (response.success) {
                            closeModal();
                            addSuccessToast(`Successfully added ${quantity} ${data.unit || ''} of ${itemName} to your grocery list.`);
                        } else {
                            alert(`Error: ${response.message || 'Failed to update quantity'}`);
                        }
                    })
                    .catch(error => {
                        console.error('Error updating quantity:', error);
                        alert('Error updating quantity. Please try again.');
                    });
                });
            }

            const addSuccessToast = (message) => {
                const existingToast = document.querySelector('.toast');
                if (existingToast) existingToast.remove();

                const toast = document.createElement('div');
                toast.className = 'toast success-toast';
                toast.textContent = message;
                document.body.appendChild(toast);

                const removeToast = () => {
                    if (toast && toast.parentNode) {
                        toast.remove();
                    }
                };

                const fadeDuration = 300; // keep in sync with CSS transition

                setTimeout(() => {
                    toast.classList.add('fade-out');
                    toast.addEventListener('transitionend', removeToast, { once: true });
                    // Safety removal in case transitionend doesn't fire
                    setTimeout(removeToast, fadeDuration + 200);
                }, 3000);
            };

            const closeModal = () => {
                ingredientPage.classList.add('hidden');
                document.body.classList.remove('modal-open');
            };

            if (newCloseButton) newCloseButton.addEventListener('click', closeModal);
            if (backdrop) backdrop.addEventListener('click', closeModal);
        }
    }


    // Add click listener to each card
    inventoryCards.forEach(card => {
        card.addEventListener('click', function() {
            const itemName = this.id;
            console.log('Clicked item:', itemName);

            fetch(`/inventory/api/${itemName}`)
                .then(res => res.json())
                .then(data => {
                    console.log('Item data:', data);
                    // Populate ingredient page with data
                    attachInnerHTML(data);
                })
                .catch(error => {
                    console.error('Error fetching item data:', error);
                });
        });
    });

    // Close ingredient page button functionality
    if (ingredientCloseButton && ingredientPage) {
        console.log("Close button pressed")
        ingredientCloseButton.addEventListener('click', function() {
            if (!ingredientPage.className.includes("hidden")){
                ingredientPage.classList.add("hidden");
            }
        });
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && ingredientPage && !ingredientPage.className.includes("hidden")) {
            ingredientPage.classList.add("hidden");
        }
    })

});
