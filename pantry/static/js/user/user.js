document.addEventListener("DOMContentLoaded", function() {
    // set random bright background color for default profile picture container
    const defaultPfpContainer = document.querySelector(".default-pfp-container");
    defaultPfpContainer.style.backgroundColor = "hsl(" + Math.floor(Math.random() * 360) + ", 100%, 75%)";

    // Add recipe link for all recipe item cards
    const recipeCards = document.querySelectorAll(".saved-recipe-item");
    recipeCards.forEach(card => {
        const recipeId = card.getAttribute("id");
        card.addEventListener("click", function() {
            window.location.href = `/recipes/${recipeId}`;
        });
    });

    // Add link for grocery list page
    const groceryListCard = document.querySelector(".shopping-list-preview-card");
    groceryListCard.addEventListener("click", function() {
        window.location.href = "/shopping";
    });
});