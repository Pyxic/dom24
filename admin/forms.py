from django import forms

from admin.models import MainPage, AboutUs, ServicePage, ContactPage, SeoText, Gallery, CustomerService


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


class SeoCreateForm(forms.ModelForm):
    class Meta:
        model = SeoText
        fields = '__all__'


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['image', 'is_additional']


class CustomerServiceForm(forms.ModelForm):
    class Meta:
        model = CustomerService
        fields = '__all__'
