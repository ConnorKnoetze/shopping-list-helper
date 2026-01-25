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

    //back button section
    const backButton = document.querySelector(".back-button");
    if (backButton) {
        backButton.addEventListener("click", function () {
            window.history.back();
        });
    }
});