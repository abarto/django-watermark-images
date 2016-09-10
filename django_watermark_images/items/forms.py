from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from .models import Item


class TextOverlayForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'text-overlay-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.layout = Layout(
            'text',
            'image',
            Submit('submit', 'Submit', css_class='btn-default pull-right')
        )

    text = forms.CharField(label='Text', max_length=100, required=True)
    image = forms.ImageField(label='Source Image', required=True)


class WatermarkForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'text-overlay-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.layout = Layout(
            'image',
            'watermark_image',
            Submit('submit', 'Submit', css_class='btn-default pull-right')
        )

    image = forms.ImageField(label='Source Image', required=True)
    watermark_image = forms.ImageField(label='Watermark Image', required=True)


class SteganographyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'text-overlay-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.layout = Layout(
            'text',
            'image',
            Submit('submit', 'Submit', css_class='btn-default pull-right')
        )

    text = forms.CharField(label='Text', max_length=500, widget=forms.Textarea, required=True)
    image = forms.ImageField(label='Source Image', required=True)


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('title', 'description', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'text-overlay-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.layout = Layout(
            'title',
            'description',
            'image',
            Submit('submit', 'Submit', css_class='btn-default pull-right')
        )
