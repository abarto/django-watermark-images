import uuid

from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


def image_upload_to(instance, filename):
    return 'original_image/{uuid}/{filename}'.format(uuid=uuid.uuid4().hex, filename=filename)


class Item(TitleDescriptionModel, TimeStampedModel):
    image = models.ImageField(_('original image'), upload_to=image_upload_to)

    def get_absolute_url(self):
        return reverse_lazy('item-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return 'Item(title={title})'.format(title=self.title)
