import setting
from PIL import Image

print(setting.ocr_dir)


def recognize_img_to_string(img_path):
    img = Image.open(img_path)
    img.show()
