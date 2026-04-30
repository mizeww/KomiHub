window.addEventListener('scroll', function() {
    const header = document.querySelector('.main-header');

    // Если прокрутили больше 100px — шапка окрашивается
    if (window.scrollY > 100) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});