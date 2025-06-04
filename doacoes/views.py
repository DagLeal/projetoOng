from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils_pix import gerar_qrcode_base64

CHAVE_PIX = "hiagoarruda25@gmail.com"  # Substitua pela chave oficial da ONG quando tiver

@csrf_exempt
def gerar_pix_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nome = data.get("nome", "DOADOR")
            cidade = "Rio de Janeiro"
            valor = float(data.get("valor", 0))
            descricao = "Doacao para ONG"

            base64_qr = gerar_qrcode_base64(CHAVE_PIX, nome, cidade, valor, descricao)
            return JsonResponse({"qr_code_base64": base64_qr})

        except Exception as e:
            return JsonResponse({"error": f"Erro ao gerar QR Code: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)
