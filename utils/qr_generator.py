import qrcode
from config.settings import settings

def generate_pix_qr():
    img = qrcode.make(settings.PIX_KEY)
    img.save("pix_qr.png")
    return "pix_qr.png"