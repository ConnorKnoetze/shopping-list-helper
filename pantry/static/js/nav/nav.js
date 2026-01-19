document.addEventListener('DOMContentLoaded', () => {
    const navOpen = document.querySelector('.nav-content.opened');
    const navClosed = document.querySelector('.nav-content.closed');
    const closeBtn = navOpen?.querySelector('.nav-close-btn');

    if (!navOpen || !navClosed || !closeBtn) return;

    navClosed.addEventListener('click', () => {
        navClosed.classList.add('hidden');
        navOpen.classList.remove('hidden');
    });

    closeBtn.addEventListener('click', () => {
        navOpen.classList.add('hidden');
        navClosed.classList.remove('hidden');
    });

    document.addEventListener('scroll' , () => {
        if (!navOpen.classList.contains('hidden')) {
            navOpen.classList.add('hidden');
            navClosed.classList.remove('hidden');
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !navOpen.classList.contains('hidden')) {
            navOpen.classList.add('hidden');
            navClosed.classList.remove('hidden');
        }
    });
});