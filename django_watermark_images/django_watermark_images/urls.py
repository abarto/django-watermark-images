"""django_watermark_images URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.contrib import admin
from django.views.generic.base import RedirectView

from items.views import (text_overlay, watermark, steganography, text_overlay_result, watermark_result,
                         steganography_result)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('text_overlay')), name='home'),
    url(r'^text_overlay/$', text_overlay, name='text_overlay'),
    url(r'^text_overlay_result/(?P<result_id>[0-9a-f]{32})/$', text_overlay_result, name='text_overlay_result'),
    url(r'^watermark/$', watermark, name='watermark'),
    url(r'^watermark_result/(?P<result_id>[0-9a-f]{32})/$', watermark_result, name='watermark_result'),
    url(r'^steganography/$', steganography, name='steganography'),
    url(r'^steganography_result/(?P<result_id>[0-9a-f]{32})/$', steganography_result, name='steganography_result')
]
