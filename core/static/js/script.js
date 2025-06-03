document.addEventListener('DOMContentLoaded', function () {
    /* Header Scroll */
    const header = document.getElementById('main-header');
    const logoImg = document.getElementById('logo-img');
    const main = document.getElementById('main-content');

    window.addEventListener('scroll', function () {
        if (window.scrollY > 50) {
            header.classList.add('shrink');
            if (window.innerWidth > 768) {
                logoImg.src = "/static/img/logo-pequena.png";
            }
            main.style.paddingTop = "5.5vh";
        } else {
            header.classList.remove('shrink');
            logoImg.src = "/static/img/logo-grande.png";
            main.style.paddingTop = "17.5vh";
        }
    });

    /* Documentos */
/*Carrosel*/
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
/*
// JS DO CARROSSEL ---------------------------------------------------------------------------------

let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}

// FIM JS DO CARROSSEL -------------------------------------------------------------------------------*/
