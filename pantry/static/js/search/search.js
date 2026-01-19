document.addEventListener('DOMContentLoaded', function() {
    const resetButton = document.querySelector('.reset-button');
    const searchInput = document.querySelector('.search-input');
    const searchFilter = document.querySelector('.search-filter');
    const searchButton = document.querySelector('.search-button');

    if (resetButton && searchInput) {
        resetButton.addEventListener('click', function(e) {
            e.preventDefault();
            searchInput.value = '';
            if (searchFilter) {
                searchFilter.value = 'name';
            }
            searchButton.click();
        });
    }
});

