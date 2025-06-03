import base64
from io import BytesIO
from datetime import datetime
import qrcode


def gerar_payload_pix(chave, nome, cidade, valor, mensagem):
    nome = nome.strip().upper()[:25]
    cidade = cidade.strip().upper()[:15]
    valor_str = f"{valor:.2f}"

    def montar_campo(id, valor):
        tamanho = f"{len(valor):02}"
        return f"{id}{tamanho}{valor}"

    payload = ""
    payload += montar_campo("00", "01")  # Payload Format Indicator
    payload += montar_campo("26", montar_campo("00", "br.gov.bcb.pix") + montar_campo("01", chave))
    payload += montar_campo("52", "0000")  # MCC
    payload += montar_campo("53", "986")  # BRL
    payload += montar_campo("54", valor_str)
    payload += montar_campo("58", "BR")
    payload += montar_campo("59", nome)
    payload += montar_campo("60", cidade)
    txid = f"ONG{datetime.now().strftime('%H%M%S')}"[:25]
    payload += montar_campo("62", montar_campo("05", txid))
    payload_sem_crc = payload + "6304"
    crc = crc16(payload_sem_crc.encode('utf-8'))
    payload += f"6304{crc}"
    return payload


def crc16(data: bytes, poly=0x1021, init_val=0xFFFF) -> str:
    crc = init_val
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ poly) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return f"{crc:04X}"


def gerar_qrcode_base64(chave, nome, cidade, valor, mensagem):
    payload = gerar_payload_pix(chave, nome, cidade, valor, mensagem)
    img = qrcode.make(payload)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')
