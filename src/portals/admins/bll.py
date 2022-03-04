import qrcode
import uuid
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.files import File


def generate_qr_code(wallet):
    wallet.qr_code = uuid.uuid4()
    wallet.save()

    qr_code_img = qrcode.make(wallet.qr_code)
    canvas = Image.new("RGB", (380, 380), "white")
    draw = ImageDraw.Draw(canvas)
    canvas.paste(qr_code_img)
    buffer = BytesIO()
    canvas.save(buffer, "PNG")
    wallet.qr_image.delete(save=True)
    wallet.qr_image.save(f'image{wallet.pk}.png', File(buffer), save=True)
    canvas.close()
