document.addEventListener('DOMContentLoaded', function () {
    /* Header Scroll */
    const header = document.getElementById('main-header');
    const logoImg = document.getElementById('logo-img');
    const main = document.getElementById('main-content');

    window.addEventListener('scroll', function () {
        if (window.scrollY > 50) {
            header.classList.add('shrink');
            if (window.innerWidth > 768) {
                logoImg.src = logoImg.dataset.small;
            }
            main.style.paddingTop = "5.5vh";
        } else {
            header.classList.remove('shrink');
            logoImg.src = "/static/img/logo-grande.png";
            main.style.paddingTop = "17.5vh";
        }
    });

    /* Carrossel */
    document.querySelectorAll('.carousel').forEach(carousel => {
        const slides = carousel.querySelectorAll('.slide');
        const container = carousel.closest('.carousel-container');

        if (container && slides.length <= 1) {
            const prevBtn = container.querySelector('.prev');
            const nextBtn = container.querySelector('.next');
            if (prevBtn) prevBtn.style.display = 'none';
            if (nextBtn) nextBtn.style.display = 'none';
        }
    });

     // Improved Dropdown Toggle
    const dropdownToggle = document.getElementById('dropdown-toggle');
    const dropdownParent = dropdownToggle?.parentElement;
    const dropdownMenu = dropdownParent?.querySelector('.dropdown-menu');

    if (dropdownToggle && dropdownParent && dropdownMenu) {
        dropdownToggle.addEventListener('click', function (e) {
            // Close all other dropdowns first
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                if (menu !== dropdownMenu) {
                    menu.classList.remove('open');
                }
            });

            // Toggle the clicked dropdown
            dropdownMenu.classList.toggle('open');
            e.stopPropagation();
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!dropdownParent.contains(e.target)) {
                dropdownMenu.classList.remove('open');
            }
        });
    }

});

window.moveSlide = function(carrosselId, direction) {
    const carousel = document.getElementById(`carousel-${carrosselId}`);
    if (!carousel) return;

    const slides = carousel.querySelectorAll('.slide');
    let currentIndex = parseInt(carousel.dataset.currentSlide || 0);

    // Pause all videos in this carousel before sliding
    carousel.querySelectorAll('video').forEach(video => {
        video.pause();
    });

    currentIndex = (currentIndex + direction + slides.length) % slides.length;
    carousel.dataset.currentSlide = currentIndex;
    carousel.style.transform = `translateX(-${currentIndex * 100}%)`;

    // Autoplay the newly visible video
    const currentVideo = slides[currentIndex].querySelector('video');
    if (currentVideo) {
        currentVideo.play().catch(e => console.log("Autoplay prevented:", e));
    }
};

