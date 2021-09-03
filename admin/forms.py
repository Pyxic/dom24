from django import forms
from django.forms import TextInput

from admin.models import MainPage, AboutUs, ServicePage, ContactPage, SeoText, Gallery, CustomerService, Document

from django.forms.widgets import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    initial_text = ''

    input_text = ''

    clear_checkbox_label = ''

    template_with_initial = (
        '%(input)s'
    )

    template_with_clear = '%(clear)s'
    '<label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'


class MainConfForm(forms.ModelForm):
    class Meta:
        model = MainPage
        exclude = ['seo']


class AboutUsConfForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        exclude = ['seo']


class ServicePageConfForm(forms.ModelForm):
    class Meta:
        model = ServicePage
        exclude = ['seo']


class ContactPageConfForm(forms.ModelForm):
    class Meta:
        model = ContactPage
        exclude = ['seo']
        widgets = {
            "phone": TextInput(attrs={
                'class': 'form-control',
                'data-mask': '(000)-000-00-00',
                'placeholder': '(000)-000-00-00'
            })
        }


class SeoCreateForm(forms.ModelForm):
    class Meta:
        model = SeoText
        fields = '__all__'


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['image', 'is_additional']


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'


class CustomerServiceForm(forms.ModelForm):
    class Meta:
        model = CustomerService
        fields = '__all__'
        widgets = {
            'image': CustomClearableFileInput
        }
