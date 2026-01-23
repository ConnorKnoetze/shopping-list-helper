document.addEventListener("DOMContentLoaded", function() {
    //sidebar section
    const recipeSidebar = document.querySelector(".recipe-sidebar")
    const windowHeight = window.innerHeight;
    let currentScroll = window.scrollY;
    let maxScroll = document.documentElement.scrollHeight - window.innerHeight;

    const breakpoint = 900; // Define the breakpoint for mobile vs desktop

    if (windowHeight > breakpoint && recipeSidebar) {
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