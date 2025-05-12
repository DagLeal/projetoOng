document.addEventListener('DOMContentLoaded', function () {
  const header = document.getElementById('main-header');
  const logoImg = document.getElementById('logo-img');

  window.addEventListener('scroll', function () {
    if (window.scrollY > 50) {
      header.classList.add('shrink');
      logoImg.src = "/static/core/img/logo-pequena.png";
    } else {
      header.classList.remove('shrink');
      logoImg.src = "/static/core/img/logo-grande.png";
    }
  });
});