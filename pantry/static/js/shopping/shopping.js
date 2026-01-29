document.addEventListener('DOMContentLoaded', function() {
    const downloadGroceryButton = document.querySelector('.download-grocery-list-button');

    if (downloadGroceryButton) {
        downloadGroceryButton.addEventListener('click', function() {
            console.log('Downloading grocery list as TXT file');
            fetch('/shopping/api/download', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then(data => {
                const blob = new Blob([data.shopping_list], { type: 'text/plain' });
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', 'grocery_list.txt');
                document.body.appendChild(link);
                link.click();
                window.URL.revokeObjectURL(url);
                link.parentNode.removeChild(link);
            })
            .catch(error => {
                console.error('Error downloading grocery list:', error);
                alert('Error downloading grocery list. Please try again.');
            });
        });
    }

    const groceryRemoveButtons = document.querySelectorAll('.remove-item-button');

    groceryRemoveButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemName = this.name;
            console.log('Removing item from grocery list:', itemName);

            fetch(`/shopping/api/remove/${itemName}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(res => res.json())
            .then(response => {
                console.log('Server response:', response);

                if (response.success) {
                    const itemElement = document.getElementById(itemName);
                    if (itemElement) {
                        itemElement.remove();

                        const groceryItemCard = document.querySelector('.grocery-item-card')

                        if (!groceryItemCard){
                            const savedRecipeCard = document.querySelector('.saved-recipe-ingredient-list-container');
                            if (!savedRecipeCard) {
                                document.querySelector('.download-grocery-list-button').remove();
                            }
                            const groceryList = document.querySelector('.grocery-list')
                            if (groceryList) {
                                window.location.reload()
                            }
                        }
                    }
                } else {
                    alert(`Error: ${response.message || 'Failed to remove item'}`);
                }
            })
            .catch(error => {
                console.error('Error removing item:', error);
                alert('Error removing item. Please try again.');
            }
            );
        }
        );
    });

    // Delete saved recipe
    const deleteRecipeButtons = document.querySelectorAll('.delete-saved-recipe-button');
    deleteRecipeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const recipeName = this.name;
            console.log('Deleting saved recipe with Name:', recipeName);

            fetch(`/shopping/api/delete_recipe/${recipeName}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(res => res.json())
            .then(response => {
                console.log('Server response:', response);

                if (response.success) {
                    const recipeElement = document.getElementById(recipeName);
                    if (recipeElement) {
                        recipeElement.remove();

                        const savedRecipeCard = document.querySelector('.saved-recipe-ingredient-list-container');
                        if (savedRecipeCard) {
                            const groceryItemCard = document.querySelector('.grocery-item-card')
                            if (!groceryItemCard) {
                                document.querySelector('.download-grocery-list-button').remove();
                            }
                            const groceryList = document.querySelector('.grocery-list')
                            if (groceryList) {
                                window.location.reload()
                            }
                        }
                    }
                } else {
                    alert(`Error: ${response.message || 'Failed to delete recipe'}`);
                }
            })
            .catch(error => {
                console.error('Error deleting recipe:', error);
                alert('Error deleting recipe. Please try again.');
            }
            );
        }
        );
    });

    // Delete Saved Recipe Required Ingredient
    const ingredientRemoveButtons = document.querySelectorAll('.remove-saved-recipe-ingredient-button');
    ingredientRemoveButtons.forEach(button => {
        button.addEventListener('click', function() {
            const recipeName = this.name.split("::")[0];
            const ingredientName = this.name.split("::")[1];
            console.log('Removing ingredient from saved recipe:', ingredientName, 'from recipe:', recipeName);

            fetch(`/shopping/api/remove_saved_recipe_ingredient/${recipeName}/${ingredientName}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(res => res.json())
            .then(response => {
                console.log('Server response:', response);

                if (response.success) {
                    const ingredientElement = document.getElementById(`${ingredientName}`);
                    if (ingredientElement) {
                        ingredientElement.remove();

                        const savedRecipeCard = document.querySelector('.saved-recipe-ingredient-list-container');
                        if (savedRecipeCard) {
                            const groceryItemCard = document.querySelector('.grocery-item-card')
                            if (!groceryItemCard) {
                                document.querySelector('.download-grocery-list-button').remove();
                            }
                            const groceryList = document.querySelector('.grocery-list')
                            if (groceryList) {
                                window.location.reload()
                            }
                        }
                    }
                } else {
                    alert(`Error: ${response.message || 'Failed to remove ingredient'}`);
                }
            })
            .catch(error => {
                console.error('Error removing ingredient:', error);
                alert('Error removing ingredient. Please try again.');
            }
            );
        }
        );
    });

});