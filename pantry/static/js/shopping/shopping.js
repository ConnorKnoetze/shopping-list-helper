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
                        if (!document.querySelector('.grocery-item-card')){
                            document.querySelector('.download-grocery-list-button').remove();
                            const groceryList = document.querySelector('.grocery-list')
                            if (groceryList) {
                                const emptyMessage = document.createElement('p');
                                emptyMessage.textContent = 'Your grocery list is empty.';
                                groceryList.appendChild(emptyMessage);
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
});