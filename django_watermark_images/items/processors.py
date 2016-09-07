import numpy as np

from io import BytesIO
from pickle import dump, load

from django.conf import settings
from PIL import Image, ImageDraw, ImageFont, ImageMath


def add_text_overlay(image, font, text):
    rgba_image = image.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    text_size_x, text_size_y = image_draw.textsize(text, font=font)
    text_xy = ((rgba_image.size[0] / 2) - (text_size_x / 2), (rgba_image.size[1] / 2) - (text_size_y / 2))
    image_draw.text(text_xy, text, font=font, fill=(255, 255, 255, 128))
    image_with_text_overlay = Image.alpha_composite(rgba_image, text_overlay)

    return image_with_text_overlay


def add_watermark(image, watermark):
    rgba_image = image.convert('RGBA')
    image_x, image_y = rgba_image.size
    rgba_watermark = watermark.convert('RGBA')

    watermark_x, _ = rgba_watermark.size
    if watermark_x > image_x:
        new_size = rgba_image.size * (image_x / watermark_x)
        rgba_watermark = rgba_watermark.resize(new_size, resample=Image.ANTIALIAS)

    _, watermark_y = rgba_watermark.size
    if watermark_y > image_y:
        new_size = rgba_image.size * (image_y / watermark_y)
        rgba_watermark = rgba_watermark.resize(new_size, resample=Image.ANTIALIAS)

    rgba_watermark_mask = rgba_watermark.convert("L").point(lambda x: min(x, 50))
    rgba_watermark.putalpha(rgba_watermark_mask)

    watermark_x, watermark_y = rgba_watermark.size
    rgba_image.paste(rgba_watermark, ((image_x - watermark_x) // 2, (image_y - watermark_y) // 2), rgba_watermark_mask)

    return rgba_image


def lsb_encode(data, image):
    bytes_io = BytesIO()
    dump(data, file=bytes_io)
    data_bytes = bytes_io.getvalue()
    data_bytes_array = np.fromiter(data_bytes, dtype=np.uint8)
    data_bits_list = np.unpackbits(data_bytes_array).tolist()
    data_bits_list += [0] * (image.size[0] * image.size[1] - len(data_bits_list))
    watermark = Image.frombytes(data=bytes(data_bits_list), size=image.size, mode='L')
    red, green, blue = image.split()
    watermarked_red = ImageMath.eval("convert(a&0xFE|b&0x1,'L')", a=red, b=watermark)
    watermarked_image = Image.merge("RGB", (watermarked_red, green, blue))
    return watermarked_image


def lsb_decode(image):
    red, green, blue = image.split()
    watermark = ImageMath.eval("(a&0x1)*0x01", a=red)
    watermark = watermark.convert('L')
    watermark_bytes = bytes(watermark.getdata())
    watermark_bits_array = np.fromiter(watermark_bytes, dtype=np.uint8)
    watermark_bytes_array = np.packbits(watermark_bits_array)
    watermark_bytes = bytes(watermark_bytes_array)
    bytes_io = BytesIO(watermark_bytes)
    return load(bytes_io)


class TextOverlay(object):
    font = ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf', 24)

    def process(self, image):
        return add_text_overlay(image, self.font, 'django-watermark-images')


class Watermark(object):
    watermark = Image.open(settings.WATERMARK_IMAGE)

    def process(self, image):
        return add_watermark(image, self.watermark)


class HiddenWatermark(object):
    def process(self, image):
        return lsb_encode('django-watermark-images', image)
