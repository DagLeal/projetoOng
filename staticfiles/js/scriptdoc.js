/*Separado para a Documentação*/


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
        } else if (['doc', 'docx'].includes(ext)) {
            container.innerHTML = `<a href="${url}" class="btn btn-primary" target="_blank">📝 Baixar Documento Word</a>`;
        } else {
            container.innerHTML = `<a href="${url}" class="btn btn-primary" target="_blank">📄 Baixar Documento</a>`;
        }
    }

    select.addEventListener("change", mostrarDocumento);
    if (select.value) mostrarDocumento();