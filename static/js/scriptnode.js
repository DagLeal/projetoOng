document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("form-doacao");

  if (!form) {
    console.error("Formulário de doação não encontrado!");
    return;
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;
    const cpf = document.getElementById("cpf").value;
    const valor = parseFloat(document.getElementById("valor").value);

    if (!valor || valor <= 0) {
      alert("Informe um valor válido para doação.");
      return;
    }

    try {
      const response = await fetch("/api/gerar-pix/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ nome, email, cpf, valor }),
      });

      if (!response.ok) {
        throw new Error("Falha ao gerar QR Code Pix.");
      }

      const data = await response.json();

      if (data.qr_code_base64) {
        const img = document.getElementById("qr-image");
        const container = document.getElementById("qr-container");

        if (img && container) {
          img.src = `data:image/png;base64,${data.qr_code_base64}`;
          container.style.display = "block";
        } else {
          console.error("Elementos do QR Code não encontrados.");
        }

      } else {
        alert("Erro ao gerar QR Code. Verifique os dados e tente novamente.");
      }

    } catch (error) {
      console.error("Erro na requisição:", error);
      alert("Erro ao conectar com o servidor de QR Code.");
    }
  });
});