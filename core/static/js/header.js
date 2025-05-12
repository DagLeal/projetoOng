document.addEventListener('DOMContentLoaded', function () {
  const header = document.getElementById('main-header');
  const logoImg = document.getElementById('logo-img');
  const main = document.getElementById('main-content');

  window.addEventListener('scroll', function () {
    if (window.scrollY > 50) {
      header.classList.add('shrink');
      logoImg.src = "/static/core/img/logo-pequena.png";
      main.style.paddingTop = "5.5vh";
    } else {
      header.classList.remove('shrink');
      logoImg.src = "/static/core/img/logo-grande.png";
      main.style.paddingTop = "17.5vh";
    }
  });
});