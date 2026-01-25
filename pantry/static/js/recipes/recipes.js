document.addEventListener("DOMContentLoaded", () => {
    const recipeCards = document.querySelectorAll(".recipe-card");

    recipeCards.forEach(card => {
        const recipeButton = card.querySelector(".view-recipes-button");
        card.addEventListener("mouseover", () => {
            recipeButton.style.opacity = "1";
            recipeButton.style.display = "block";
        });
        card.addEventListener("mouseout", () => {
            const recipeButton = card.querySelector(".view-recipes-button");
            recipeButton.style.opacity = "0";
            recipeButton.style.display = "none";
        });

        card.addEventListener("click", (e) => {
            if (e.button === 2) return; // Ignore right-clicks
            const recipeName = card.getAttribute("data-recipe-name").replaceAll(' ', '-').toLowerCase();
            let selection = window.getSelection().toString();
            if (e.button === 0 && !selection) {
                window.location.href = `/recipes/${recipeName}`;
            }
            else if (e.button === 1 && !selection) {
                window.open(`/recipes/${recipeName}`, '_blank');
            }
        });
    });
});