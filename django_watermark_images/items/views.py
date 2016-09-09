from django.views.generic import TemplateView


class TextOverlay(TemplateView):
    template_name = 'items/text_overlay.html'
text_overlay = TextOverlay.as_view()


class Watermark(TemplateView):
    template_name = 'items/watermark.html'
watermark = Watermark.as_view()


class Steganography(TemplateView):
    template_name = 'items/steganography.html'
steganography = Steganography.as_view()
