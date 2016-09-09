from django.views.generic import TemplateView, FormView

from .forms import TextOverlayForm, WatermarkForm, SteganographyForm


class TextOverlay(FormView):
    template_name = 'items/text_overlay.html'
    form_class = TextOverlayForm
text_overlay = TextOverlay.as_view()


class Watermark(FormView):
    template_name = 'items/watermark.html'
    form_class = WatermarkForm
watermark = Watermark.as_view()


class Steganography(FormView):
    template_name = 'items/steganography.html'
    form_class = SteganographyForm
steganography = Steganography.as_view()
