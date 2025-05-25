document.addEventListener('DOMContentLoaded', function () {
  const header = document.getElementById('main-header');
  const logoImg = document.getElementById('logo-img');
  const main = document.getElementById('main-content');

  window.addEventListener('scroll', function () {
    if (window.scrollY > 50) {
      header.classList.add('shrink');
      logoImg.src = "/static/img/logo-pequena.png";
      main.style.paddingTop = "5.5vh";
    } else {
      header.classList.remove('shrink');
      logoImg.src = "/static/img/logo-grande.png";
      main.style.paddingTop = "17.5vh";
    }
  });
});


function mostrarImagem() {
    const select = document.getElementById('documentoSelect');
    const img = document.getElementById('imagemSelecionada');
    const url = select.value;

    if (url) {
        img.src = url;
        img.style.display = 'block';
    } else {
        img.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('documentoSelect').addEventListener('change', mostrarImagem);
});

