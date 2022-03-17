import qrcode as qc
import uuid
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.files import File


def generate_qr_code(wallet):
    wallet.qr_code = uuid.uuid4()
    wallet.save()

    qr_code_img = qc.make(wallet.qr_code)
    canvas = Image.new("RGB", (380, 380), "white")
    draw = ImageDraw.Draw(canvas)
    canvas.paste(qr_code_img)
    buffer = BytesIO()
    canvas.save(buffer, "PNG")
    wallet.qr_image.delete(save=True)
    wallet.qr_image.save(f'image{wallet.pk}.png', File(buffer), save=True)
    canvas.close()


def check_sanction_for_web(sanction, sanction_type):
    is_allowed = False

    if sanction_type == 'top_up' and sanction.is_top_up_allowed:
        is_allowed = True
    elif sanction_type == 'transaction' and sanction.is_transaction_allowed:
        is_allowed = True
    elif sanction_type == 'withdrawal' and sanction.is_withdrawal_allowed:
        is_allowed = True

    return is_allowed
