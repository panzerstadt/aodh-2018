import base64, io
from PIL import Image


def base64_to_image(input_b64):
    """
    INPUT conversion (API)
    converts b64 to image OBJECT (to be passed into scipy.misc.imread() to convert into an np array
    :param input_b64:
    :return: similar to open(fp).read()
    """
    decoded_img = base64.b64decode(input_b64)
    output_img_obj = io.BytesIO(decoded_img)
    return output_img_obj


def show_base64_image(base64_str):
    im_bytes = base64_to_image(base64_str)
    im_content = Image.open(im_bytes)
    im_content.show()


def save_base64_image(base64_str, fp):
    im_bytes = base64_to_image(base64_str)
    im_content = Image.open(im_bytes)
    im_content.save(fp, 'PNG')