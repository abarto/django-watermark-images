from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
from imagekit.models import ImageSpecField

from .processors import TextOverlay, Watermark, HiddenWatermark


class Item(TitleDescriptionModel, TimeStampedModel):
    original_image = models.ImageField(_('original image'))
    text_overlay_image = ImageSpecField(source='original_image', processors=[TextOverlay()], format='JPEG')
    watermark_image = ImageSpecField(source='original_image', processors=[Watermark()], format='JPEG')
    hidden_watermark_image = ImageSpecField(source='original_image', processors=[HiddenWatermark()], format='PNG')
