import math

from django import forms
from django.forms import TextInput

from account.models import Profile, Owner
from admin.models import MainPage, AboutUs, ServicePage, ContactPage, SeoText, Gallery, CustomerService, Document, \
    NearBlock, Unit, Service, Tariff, TariffService, Requisites, House, Section, Level, Flat, Counter, BankBook, \
    PaymentItem, CashBox, Receipt, ReceiptService

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
    image1 = forms.ImageField(required=False, error_messages={'invalid': "Только изображения"}, widget=forms.FileInput,
                              label="Изображение #1. Размер: (522x350)")
    image2 = forms.ImageField(required=False, error_messages={'invalid': "Только изображения"}, widget=forms.FileInput,
                              label="Изображение #2. Размер: (248x160)")
    image3 = forms.ImageField(required=False, error_messages={'invalid': "Только изображения"}, widget=forms.FileInput,
                              label="Изображение #3. Размер: (248x160)")
    image4 = forms.ImageField(required=False, error_messages={'invalid': "Только изображения"}, widget=forms.FileInput,
                              label="Изображение #4. Размер: (248x160)")
    image5 = forms.ImageField(required=False, error_messages={'invalid': "Только изображения"}, widget=forms.FileInput,
                              label="Изображение #5. Размер: (248x160)")

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


class FlatCreateForm(forms.ModelForm):
    house = forms.ModelChoiceField(
        label='Дом',
        queryset=House.objects.all(), empty_label='Выберите...',
        widget=forms.Select(attrs={'class': 'form-control'}))
    section = forms.ModelChoiceField(
        required=False,
        queryset=Section.objects.all(),
        label='Секция',
        empty_label='Выберите...',
        widget=forms.Select(attrs={'class': 'form-control'}))
    level = forms.ModelChoiceField(
        required=False,
        queryset=Level.objects.all(),
        label='Этаж',
        empty_label='Выберите...',
        widget=forms.Select(attrs={'class': 'form-control'}))
    owner = forms.ModelChoiceField(
        required=False,
        queryset=Owner.objects.all(),
        label='Владелец',
        empty_label='Выберите...',
        widget=forms.Select(attrs={'class': 'form-control'}))
    bank_book = forms.ModelChoiceField(
        required=False,
        queryset=BankBook.objects.filter(flat_id=None, status='Активен'),
        label='Лицевой счет',
        empty_label='Выберите...',
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Flat
        fields = '__all__'


class FlatFilterForm(forms.Form):
    number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'data-number': '1'}))
    house = forms.ModelChoiceField(queryset=House.objects.all(), empty_label='',
                                   widget=forms.Select(attrs={'class': 'form-control', 'data-number': '2'}))
    section = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'data-number': '3'}))
    level = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'data-number': '4'}))
    owner = forms.ModelChoiceField(queryset=Owner.objects.all(), empty_label='',
                                   widget=forms.Select(attrs={'class': 'form-control', 'data-number': '5'}))


class CounterFilterForm(forms.Form):
    flat__house_id = forms.ModelChoiceField(queryset=House.objects.all(), empty_label='',
                                            widget=forms.Select(attrs={'class': 'form-control', 'data-number': '1'}))
    section = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'data-number': '2'}))
    flat__number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'data-number': '3'}))
    service = forms.ModelChoiceField(queryset=Service.objects.all(), empty_label='',
                                     widget=forms.Select(attrs={'class': 'form-control', 'data-number': '4'}))


class FlatCounterFilterForm(CounterFilterForm):
    id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'data-number': '5'}))
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'data-number': '6'}))
    date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'data-number': '7'}))


class BankBookFilterForm(forms.Form):
    id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    flat__house_id = forms.ModelChoiceField(queryset=House.objects.all(), empty_label='',
                                            widget=forms.Select(attrs={'class': 'form-control'}))
    section = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    flat__number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    flat__owner_id = forms.ModelChoiceField(queryset=Owner.objects.all(), empty_label='',
                                            widget=forms.Select(attrs={'class': 'form-control'}))


class CashBoxFilterForm(forms.Form):
    id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    payment_type_id = forms.ModelChoiceField(queryset=PaymentItem.objects.all(), empty_label='',
                                             widget=forms.Select(attrs={'class': 'form-control'}))
    bankbook__flat__owner_id = forms.ModelChoiceField(queryset=Owner.objects.all(), empty_label='',
                                                      widget=forms.Select(attrs={'class': 'form-control'}))
    bankbook_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class CounterCreateForm(forms.ModelForm):
    house = forms.ModelChoiceField(
        label='Дом',
        queryset=House.objects.all(), empty_label='Выберите...',
        widget=forms.Select(attrs={'class': 'form-control'}))
    section = forms.ModelChoiceField(
        required=False,
        queryset=Section.objects.all(),
        label='Секция',
        empty_label='Выберите...',
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Counter
        fields = '__all__'


class BankbookCreateForm(forms.ModelForm):
    house = forms.ModelChoiceField(
        label='Дом', required=False,
        queryset=House.objects.all(), empty_label='Выберите...',
        widget=forms.Select(attrs={'class': 'form-control'}))
    section = forms.ModelChoiceField(
        required=False,
        queryset=Section.objects.all(),
        label='Секция',
        empty_label='Выберите...',
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = BankBook
        fields = '__all__'


class CashBoxIncomeCreateForm(forms.ModelForm):
    owner = forms.ModelChoiceField(
        required=False,
        label='Владелец',
        queryset=Owner.objects.all(), empty_label='Выберите...',
        widget=forms.Select(attrs={'class': 'form-control'}))
    payment_type = forms.ModelChoiceField(
        label='Тип платежа', queryset=PaymentItem.objects.filter(type='приходы'),
        required=False, empty_label='Выберите...',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CashBox
        fields = '__all__'
        widgets = {
            "type": forms.HiddenInput(attrs={
                'value': 'приход'
            })
        }


class CashBoxExpenseCreateForm(forms.ModelForm):
    payment_type = forms.ModelChoiceField(
        label='Тип платежа', queryset=PaymentItem.objects.filter(type='расходы'),
        required=False, empty_label='Выберите...',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CashBox
        exclude = ['bankbook']
        widgets = {
            "type": forms.HiddenInput(attrs={
                'value': 'расход'
            })
        }

    def clean_amount_of_money(self):
        return math.fabs(self.cleaned_data['amount_of_money'])


class ReceiptCreateForm(forms.ModelForm):
    house = forms.ModelChoiceField(
        label='Дом',
        queryset=House.objects.all(), empty_label='Выберите...',
        widget=forms.Select(attrs={'class': 'form-control'}))
    section = forms.ModelChoiceField(
        required=False,
        queryset=Section.objects.all(),
        label='Секция',
        empty_label='Выберите...',
        widget=forms.Select(attrs={'class': 'form-control'}))
    bankbook = forms.CharField(label='Лицевой счет', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Receipt
        exclude = ['services']


class ReceiptServiceForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        required=False,
        queryset=Service.objects.all(),
        label='Услуга',
        empty_label='Выберите...',
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = ReceiptService
        fields = '__all__'
