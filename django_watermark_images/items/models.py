from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
from imagekit.models import ImageSpecField


class TextOverlay(object):
    def process(self, image):
        return image


class Watermark(object):
    def process(self, image):
        return image


class HiddenWattermark(object):
    def process(self, image):
        return image


class Item(TitleDescriptionModel, TimeStampedModel):
    original_image = models.ImageField(_('original image'))
    text_overlay_image = ImageSpecField(source='original_image', processors=[TextOverlay()], format='JPEG')
    watermark_image = ImageSpecField(source='original_image', processors=[Watermark()], format='JPEG')
    hidden_watermark_image = ImageSpecField(source='original_image', processors=[HiddenWattermark()], format='JPEG')
