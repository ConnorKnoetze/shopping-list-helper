document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.querySelector('.carousel-slide');
    if (!carousel) return;

    carousel.addEventListener('click', () => {
       window.location = '/recipes';
    });

    const inner = carousel.querySelector('.carousel-inner');
    const items = Array.from(inner.querySelectorAll('.carousel-item'));

    if (items.length === 0) return;

    let currentIndex = 0;
    let isTransitioning = false;
    let autoPlayInterval;

    // Clone first and last slides for infinite effect
    const firstClone = items[0].cloneNode(true);
    const lastClone = items[items.length - 1].cloneNode(true);

    firstClone.classList.remove('active');
    lastClone.classList.remove('active');

    inner.appendChild(firstClone);
    inner.insertBefore(lastClone, items[0]);

    // Update items array to include clones
    const allItems = Array.from(inner.querySelectorAll('.carousel-item'));
    const totalSlides = allItems.length;

    // Set initial position (start at index 1 because we added a clone at the beginning)
    currentIndex = 1;
    inner.style.transform = `translateX(-${currentIndex * 100}%)`;

    // Function to move to a specific slide
    function goToSlide(index, withTransition = true) {
        if (isTransitioning && withTransition) return;

        if (withTransition) {
            isTransitioning = true;
            inner.style.transition = 'transform 0.5s ease-in-out';
        } else {
            inner.style.transition = 'none';
        }

        inner.style.transform = `translateX(-${index * 100}%)`;
        currentIndex = index;

        // Update active class
        allItems.forEach(item => item.classList.remove('active'));
        allItems[currentIndex].classList.add('active');

        // If no transition, we're done immediately
        if (!withTransition) {
            // Re-enable transitions after the instant jump
            setTimeout(() => {
                inner.style.transition = 'transform 0.5s ease-in-out';
            }, 50);
        }
    }

    // Handle the infinite loop transition
    function handleTransitionEnd() {
        // If we're at the first clone (after last real slide), jump to real first slide
        if (currentIndex === totalSlides - 1) {
            currentIndex = 1;
            goToSlide(currentIndex, false);
        }
        // If we're at the last clone (before first real slide), jump to real last slide
        else if (currentIndex === 0) {
            currentIndex = totalSlides - 2;
            goToSlide(currentIndex, false);
        }

        isTransitioning = false;
    }

    inner.addEventListener('transitionend', handleTransitionEnd);

    // Next slide function
    function nextSlide() {
        if (isTransitioning) return;
        goToSlide(currentIndex + 1);
    }

    // Previous slide function
    function prevSlide() {
        if (isTransitioning) return;
        goToSlide(currentIndex - 1);
    }

    // Auto-play functionality
    function startAutoPlay() {
        autoPlayInterval = setInterval(nextSlide, 4000);
    }

    function stopAutoPlay() {
        if (autoPlayInterval) {
            clearInterval(autoPlayInterval);
        }
    }

    function resetAutoPlay() {
        stopAutoPlay();
        startAutoPlay();
    }

    // Start auto-play
    startAutoPlay();

    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            inner.style.transition = 'none';
            inner.style.transform = `translateX(-${currentIndex * 100}%)`;
            setTimeout(() => {
                inner.style.transition = 'transform 0.5s ease-in-out';
            }, 50);
        }, 250);
    });
});