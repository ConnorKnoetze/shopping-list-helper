document.addEventListener("DOMContentLoaded", () => {
    const titleButton = document.querySelector(".hero-section");
    titleButton.addEventListener("click", () => {
        window.location.href = "/recipes";
    });

    const viewRecipesButton = document.querySelector(".view-recipes-button");
    viewRecipesButton.addEventListener("click", () => {
        window.location.href = "/recipes";
    });

    const shoppingNavButton = document.querySelector(".shopping-nav-button");
    const ingredientsGrid = document.querySelector(".ingredients-grid");

    const isTouchScreen = 'ontouchstart' in document.documentElement;

    if (!isTouchScreen) {
        ingredientsGrid.addEventListener('mouseenter', () => {
            shoppingNavButton.classList.add("visible");
        });

        ingredientsGrid.addEventListener('mouseleave', () => {
            shoppingNavButton.classList.remove("visible");
        });

        shoppingNavButton.addEventListener("click", () => {
            window.location.href = "/inventory";
        });

        shoppingNavButton.addEventListener('mouseenter', () => {
            shoppingNavButton.classList.add("visible");
        });


    } else {
        shoppingNavButton.classList.add("visible");
        shoppingNavButton.addEventListener("click", () => {
            window.location.href = "/inventory";
        });
    }
});