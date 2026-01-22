document.addEventListener("DOMContentLoaded", () => {
    const recipeCards = document.querySelectorAll(".recipe-card");

    recipeCards.forEach(card => {
        card.addEventListener("click", () => {
            const recipeName = card.getAttribute("data-recipe-name").replaceAll(' ', '-').toLowerCase();
            window.location.href = `/recipes/${recipeName}`;
        });
    });
});