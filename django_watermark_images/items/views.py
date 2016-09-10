import uuid

from functools import lru_cache
from io import BytesIO

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, View

from magic import Magic
from PIL import Image, ImageFont

from .forms import TextOverlayForm, WatermarkForm, SteganographyForm
from .processors import add_text_overlay, add_watermark, lsb_encode, lsb_decode


@lru_cache(maxsize=1)
def _get_placeholder_image_bytes():
    with open(settings.PLACEHOLDER_IMAGE, 'rb') as fp:
        return fp.read()


def _create_result_id():
    return uuid.uuid4().hex


def _get_cache_key(prefix, result_id):
    return '{prefix}-image-{result_id}'.format(prefix=prefix, result_id=result_id)


def _get_source_image_key(result_id):
    return _get_cache_key('source', result_id)


def _get_result_image_key(result_id):
    return _get_cache_key('result', result_id)


def _save_image(key, image, format='png'):
    bytes_io = BytesIO()
    image.save(bytes_io, format=format)
    cache.set(key, bytes_io.getvalue())


def _save_source_image(image, result_id):
    _save_image(_get_source_image_key(result_id), image, format=image.format)


def _save_result_image(image, result_id):
    _save_image(_get_result_image_key(result_id), image)


def _get_image(key):
    image_bytes = cache.get(key)

    if image_bytes is None:
        image_bytes = _get_placeholder_image_bytes()

    image_fp = BytesIO(image_bytes)
    return image_fp


class TextOverlay(FormView):
    template_name = 'items/text_overlay.html'
    form_class = TextOverlayForm

    def form_valid(self, form):
        text = form.cleaned_data['text']
        image = Image.open(form.cleaned_data['image'])

        font = ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf', 24)
        result_image = add_text_overlay(image, font, text)

        result_id = _create_result_id()
        _save_source_image(image, result_id)
        _save_result_image(result_image, result_id)

        return HttpResponseRedirect(reverse_lazy('text_overlay_result', kwargs={'result_id': result_id}))
text_overlay = TextOverlay.as_view()


class TextOverlayResult(TemplateView):
    template_name = 'items/text_overlay_result.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        result_id = kwargs.get('result_id', 'unknown')
        context_data['source_image_src'] = reverse_lazy('cached_image', kwargs={'key': _get_source_image_key(result_id)})
        context_data['result_image_src'] = reverse_lazy('cached_image', kwargs={'key': _get_result_image_key(result_id)})
        return context_data
text_overlay_result = TextOverlayResult.as_view()


class Watermark(FormView):
    template_name = 'items/watermark.html'
    form_class = WatermarkForm


    def form_valid(self, form):
        image = Image.open(form.cleaned_data['image'])
        watermark_image = Image.open(form.cleaned_data['watermark_image'])

        result_image = add_watermark(image, watermark_image)

        result_id = _create_result_id()
        _save_source_image(image, result_id)
        _save_result_image(result_image, result_id)

        return HttpResponseRedirect(reverse_lazy('watermark_result', kwargs={'result_id': result_id}))
watermark = Watermark.as_view()


class WatermarkResult(TemplateView):
    template_name = 'items/watermark_result.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        result_id = kwargs.get('result_id', 'unknown')
        context_data['source_image_src'] = reverse_lazy('cached_image', kwargs={'key': _get_source_image_key(result_id)})
        context_data['result_image_src'] = reverse_lazy('cached_image', kwargs={'key': _get_result_image_key(result_id)})
        return context_data
watermark_result = WatermarkResult.as_view()


class Steganography(FormView):
    template_name = 'items/steganography.html'
    form_class = SteganographyForm
steganography = Steganography.as_view()


class SteganographyResult(TemplateView):
    template_name = 'items/steganography_result.html'
steganography_result = SteganographyResult.as_view()


class CachedImage(View):
    def get(self, request, key=None, **kwargs):
        image_fp = _get_image(key)
        magic = Magic(mime=True)
        content_type = magic.from_buffer(image_fp.read(1024))
        image_fp.seek(0)
        return HttpResponse(image_fp, content_type=content_type)
cached_image = CachedImage.as_view()
