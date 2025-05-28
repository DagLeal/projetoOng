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
    const documentos = JSON.parse(
        document.getElementById('documentos-json').textContent
    );

    const select = document.getElementById("documentoSelect");
    const container = document.getElementById("documentoSelecionado");
    const downloadDiv = document.getElementById("botaoDownload");

    function mostrarDocumento() {
        const id = select.value;
        const doc = documentos.find(d => d.pk == id);

        if (!doc) {
            container.innerHTML = "";
            downloadDiv.innerHTML = "";
            return;
        }

        const path = doc.fields.arquivo.startsWith('/') ? doc.fields.arquivo : '/' + doc.fields.arquivo;
        const url = "/media" + path;
        const ext = url.split('.').pop().toLowerCase();

        // Botão de download (só para PDF)
        if (ext === 'pdf') {
            downloadDiv.innerHTML = `<a href="${url}" class="btn btn-success" download>⬇️ Baixar PDF</a>`;
        } else {
            downloadDiv.innerHTML = "";
        }

        // Exibição do conteúdo
        if (['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'].includes(ext)) {
            container.innerHTML = `<img src="${url}" style="max-width: 90%; height: auto;">`;
        } else if (ext === 'pdf') {
            container.innerHTML = `<iframe src="${url}" width="90%" height="800px"></iframe>`;
        } else if (['xls', 'xlsx', 'csv'].includes(ext)) {
            container.innerHTML = `<a href="${url}" class="btn btn-primary" target="_blank">📊 Baixar Planilha</a>`;
        } else {
            container.innerHTML = `<a href="${url}" class="btn btn-primary" target="_blank">📄 Baixar Documento</a>`;
        }
    }

    select.addEventListener("change", mostrarDocumento);
    if (select.value) mostrarDocumento();

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
    if (!carousel) {
        console.error("Carousel not found:", `carousel-${carrosselId}`);
        return;
    }

    const slides = carousel.querySelectorAll('.slide');
    let currentIndex = parseInt(carousel.dataset.currentSlide || 0);

    currentIndex += direction;

    // Handle wrap-around
    if (currentIndex < 0) currentIndex = slides.length - 1;
    else if (currentIndex >= slides.length) currentIndex = 0;

    // Update the index and apply transform
    carousel.dataset.currentSlide = currentIndex;
    carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
};
