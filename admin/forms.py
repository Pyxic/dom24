from django import forms
from django.forms import TextInput

from account.models import Profile
from admin.models import MainPage, AboutUs, ServicePage, ContactPage, SeoText, Gallery, CustomerService, Document, \
    NearBlock, Unit, Service, Tariff, TariffService, Requisites, House, Section, Level

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


class NearBlockForm(forms.ModelForm):
    class Meta:
        model = NearBlock
        fields = '__all__'


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'


class ServiceForm(forms.ModelForm):
    unit = forms.ModelChoiceField(
        label='Едм. изм.',
        queryset=Unit.objects.all(), empty_label='Выберите...', required=False)

    class Meta:
        model = Service
        fields = '__all__'


class TariffCreateForm(forms.ModelForm):

    class Meta:
        model = Tariff
        fields = '__all__'


class TariffServiceForm(forms.ModelForm):
    unit = forms.ModelChoiceField(
        label='Едм. изм.',
        queryset=Unit.objects.all(), empty_label='Выберите...', disabled=True, required=False)

    service = forms.ModelChoiceField(
        label='Услуга',
        queryset=Service.objects.all(), empty_label='Выберите...')

    class Meta:
        model = TariffService
        fields = '__all__'
        widgets = {
            'currency': forms.TextInput(attrs={'readonly': 'readonly', 'value': 'грн'}),
        }


class RequisitesForm(forms.ModelForm):

    class Meta:
        model = Requisites
        fields = '__all__'


class HouseCreateForm(forms.ModelForm):

    class Meta:
        model = House
        exclude = ['users']


class SectionForm(forms.ModelForm):

    class Meta:
        model = Section
        exclude = ['house']


class LevelForm(forms.ModelForm):

    class Meta:
        model = Level
        exclude = ['house']


class HouseUserForm(forms.ModelForm):
    profile = forms.ModelChoiceField(
        label='ФИО',
        queryset=Profile.objects.all(), empty_label='Выберите...',
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = House.users.through
        fields = ['profile']
