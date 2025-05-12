from pix import Pix
import qrcode
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .models import Pagamento
from datetime import datetime


def gerar_pix(valor, chave_pix):
    pix = Pix()

    # Gerar o QR Code do Pix
    dados_qr = pix.generate_qr_code(chave=chave_pix, valor=valor)

    # Criar o QR Code como imagem
    img = qrcode.make(dados_qr)

    # Salvar a imagem em um buffer de memória
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer


def enviar_email(relatorio):
    remetente = 'seu-email@dominio.com'
    destinatario = 'destinatario@dominio.com'
    senha = 'sua-senha'

    # Criando a estrutura do e-mail
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = 'Relatório de Pagamentos do Mês'

    msg.attach(MIMEText(relatorio, 'plain'))

    # Enviar o e-mail via servidor SMTP
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg.as_string())

def gerar_relatorio_mensal():
    hoje = datetime.utcnow()
    primeiro_dia = hoje.replace(day=1)
    ultimo_dia = hoje.replace(month=hoje.month + 1 if hoje.month < 12 else 1)

    pagamentos = Pagamento.objects.filter(data_gte=primeiro_dia, data_lt=ultimo_dia)

    total = sum([p.valor for p in pagamentos])
    relatorio = f"Relatório de Pagamentos - {primeiro_dia.strftime('%B %Y')}\n\n"

    for pagamento in pagamentos:
        relatorio += f"CPF: {pagamento.cpf} | Valor: R${pagamento.valor} | Data: {pagamento.data.strftime('%d/%m/%Y %H:%M:%S')}\n"

    relatorio += f"\nTotal arrecadado: R${total}"

    enviar_email(relatorio)

