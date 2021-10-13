import json

import xlwt
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.db.models import Sum
from django.forms import modelformset_factory
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Create your views here.
from django.urls import reverse_lazy
from django.utils.dateparse import postgres_interval_re
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView, ListView, CreateView, UpdateView, DetailView
from django.views.generic.edit import FormMixin

from account.forms import UserChangeForm, ProfileChangeForm, OwnerFilterForm
from account.models import Profile, Owner
from account.services.profile import has_access, has_access_for_class
from admin.admin import CashBoxResource
from admin.forms import SeoCreateForm, GalleryForm, FlatFilterForm, CounterFilterForm, FlatCounterFilterForm, \
    BankBookFilterForm, CashBoxFilterForm, CashBoxIncomeCreateForm, CashBoxExpenseCreateForm, MasterRequestForm, \
    MessageForm, MasterRequestFilterForm, HouseFilterForm, ReceiptFilterForm
from admin.models import SeoText, Gallery, Document, Service, Unit, Tariff, Requisites, PaymentItem, House, Flat, \
    Section, Level, Counter, BankBook, CashBox, Receipt, MasterRequest, Message, ServicePage, CustomerService
from admin.services import utils
from admin.services.bankbook import BankbookData
from admin.services.cashbox import CashBoxMixin, CashBoxData, FilterMixin
from admin.services.counter import CounterData, filter_flat_counter
from admin.services.flat import FlatData
from admin.services.house import HouseData
from admin.services.master_request import MasterRequestData
from admin.services.owner import OwnerData
from admin.services.receipt import ReceiptData, get_receipt_service_data
from admin.services.services import UnitData, ServiceData, TariffData, get_roles_form
from admin.services.singleton_pages import get_singleton_page_data, RequisitesPageData


# import the logging library
import logging

# Get an instance of a logger
from admin.services.statistic import StatisticData, StatisticMixin

logger = logging.getLogger(__name__)


@has_access(permission_page='Статистика')
def index(request):
    user = User.objects.get(id=request.user.id)
    logger.info(user.profile.role)
    statistics = StatisticData()
    return render(request, 'admin/statistic.html',
                  {'statistic': statistics})


@has_access(permission_page='Управление сайтом')
def singleton_page(request, page_name):
    singleton_data = get_singleton_page_data(page_name)
    if request.method == 'POST':
        singleton_data.save_data(request.POST, request.FILES)
        return redirect(f"admin:{page_name}", page_name)
    return render(request, singleton_data.render_url, singleton_data.get_content())


@has_access(permission_page='Управление сайтом')
def delete_from_gallery(request, image_id):
    Gallery.objects.get(id=image_id).delete()
    return JsonResponse({'image_id': image_id})


@has_access(permission_page='Управление сайтом')
def delete_service_page(request, service_id):
    CustomerService.objects.filter(id=service_id).delete()
    return redirect('admin:service_page', 'service_page')


@has_access(permission_page='Услуги')
def edit_services(request):
    unit_data = UnitData()
    unit_formset = unit_data.get_formset()
    service_data = ServiceData()
    formset = service_data.get_formset()
    if request.method == 'POST':
        unit_formset = unit_data.get_formset(post=request.POST)
        formset = service_data.get_formset(post=request.POST)
        if unit_formset.is_valid() and formset.is_valid():
            unit_formset.save()
            formset.save()
    return render(request, 'admin/settings/services.html', {
        "unit_formset": unit_formset,
        "formset": formset,
    })


@has_access(permission_page='Управление сайтом')
def delete_document(request, pk):
    Document.objects.get(pk=pk).delete()
    return JsonResponse({'pk': pk})


@has_access(permission_page='Услуги')
@require_POST
def delete_service(request):
    pk = request.POST.get('pk')
    Service.objects.get(pk=pk).delete()
    return JsonResponse({'pk': pk})


@has_access(permission_page='Услуги')
@require_POST
def delete_unit(request):
    pk = request.POST.get('pk')
    Unit.objects.get(pk=pk).delete()
    return JsonResponse({'pk': pk})


class TariffList(UserPassesTestMixin, ListView):
    model = Tariff
    template_name = 'admin/settings/tariff/index.html'

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Тарифы', user=current_user)


@has_access(permission_page='Тарифы')
def update_tariff(request, tariff_id=None, clone=False):
    tariff = TariffData(tariff_id, bool(clone))
    form = tariff.get_form(instance=True)
    formset = tariff.get_formset()
    if request.method == 'POST':
        if tariff.save_data(request.POST) is True:
            return redirect("admin:tariff_list")
    return render(request, 'admin/settings/tariff/update.html',
                  {"form": form,
                   "formset": formset,
                   "update": True if tariff_id else False})


@has_access(permission_page='Тарифы')
def delete_tariff(request, tariff_id):
    Tariff.objects.get(id=tariff_id).delete()
    return redirect('admin:tariff_list')


def get_unit_by_service(request):
    if request.is_ajax():
        unit = Service.objects.get(id=request.GET.get('id')).unit_id
        return HttpResponse(unit)


@has_access(permission_page='Роли')
def settings_roles(request):
    forms = get_roles_form()
    if request.method == 'POST':
        logger.info(request.POST.dict())
        forms = get_roles_form(post=request.POST)
        for key, role in forms.items():
            for form in role:
                if form.is_valid():
                    form.save()
        messages.success(request, 'Права успешно изменены')
    return render(request, 'admin/settings/roles.html', {
        'forms': forms
    })


class UserList(UserPassesTestMixin, ListView):
    model = User
    template_name = 'admin/settings/user/index.html'

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Пользователи', user=current_user)

    def get_queryset(self, **kwargs):
        qs = super(UserList, self).get_queryset(**kwargs)
        qs = qs.exclude(id__in=Owner.objects.all().values_list('user_id'))
        return qs


@has_access(permission_page='Пользователи')
def update_user(request, user_id=None):
    if user_id is None:
        user = User()
        profile = Profile()
    else:
        user = User.objects.get(id=user_id)
        profile, _ = Profile.objects.get_or_create(user_id=user_id)
    register_form = UserChangeForm(instance=user)
    profile_form = ProfileChangeForm(instance=profile)
    if request.method == 'POST':
        register_form = UserChangeForm(request.POST, instance=user)
        profile_form = ProfileChangeForm(request.POST, instance=profile)
        if register_form.is_valid() and profile_form.is_valid():
            updated_user = register_form.save(commit=False)
            updated_user.username = register_form.cleaned_data['email']
            if 'password' in register_form.changed_data:
                updated_user.set_password(register_form.cleaned_data['password'])
            updated_user.save()
            updated_profile = profile_form.save(commit=False)
            updated_profile.user_id = updated_user.id
            updated_profile.save()
            return redirect("admin:user_list")
    return render(request, "admin/settings/user/update.html",
                  {
                      "register_form": register_form,
                      "profile_form": profile_form
                  })


@has_access(permission_page='Пользователи')
def delete_user(request, user_id):
    User.objects.get(id=user_id).delete()
    return redirect('admin:user_list')


@has_access(permission_page='Платежные реквизиты')
def settings_requisites(request):
    requisites_data = RequisitesPageData()
    if request.method == 'POST':
        requisites_data.save_data(request.POST)
        messages.success(request, 'Реквизиты успешно сохранены')
        return redirect(f"admin:requisites")
    return render(request, requisites_data.render_url, requisites_data.get_content())


class PaymentItemList(UserPassesTestMixin, ListView):
    model = PaymentItem
    template_name = 'admin/settings/payment_item/index.html'

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Платежные реквизиты', user=current_user)


class PaymentItemCreateView(CreateView):
    model = PaymentItem
    template_name = 'admin/settings/payment_item/create.html'
    fields = ['name', 'type']
    success_url = reverse_lazy('admin:payment_item_list')


class PaymentItemUpdateView(UpdateView):
    model = PaymentItem
    template_name = 'admin/settings/payment_item/update.html'
    fields = ['name', 'type']
    success_url = reverse_lazy('admin:payment_item_list')


def delete_payment_item(request, payment_item_id):
    PaymentItem.objects.get(id=payment_item_id).delete()
    return redirect('admin:payment_item_list')


class HouseList(UserPassesTestMixin, FormMixin, FilterMixin, ListView):
    model = House
    form_class = HouseFilterForm
    template_name = 'admin/house/house/index.html'

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Дома', user=current_user)


class HouseDetail(UserPassesTestMixin, DetailView):
    model = House
    template_name = 'admin/house/house/detail.html'

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Дома', user=current_user)


@has_access(permission_page='Дома')
def update_house(request, house_id=None):
    house = HouseData(house_id)
    form = house.get_form(instance=True)
    section_formset = house.get_section_formset()
    level_formset = house.get_level_formset()
    user_formset = house.get_user_formset()
    if request.method == 'POST':
        if house.save_data(request.POST, request.FILES) is True:
            return redirect("admin:house_list")
    return render(request, 'admin/house/house/update.html',
                  {"form": form,
                   "section_formset": section_formset,
                   "level_formset": level_formset,
                   "user_formset": user_formset})


@has_access(permission_page='Дома')
def delete_house(request, house_id):
    House.objects.get(id=house_id).delete()
    return redirect('admin:house_list')


def delete_section(request, pk):
    Section.objects.get(pk=pk).delete()
    return JsonResponse({'pk': pk})


def delete_level(request, pk):
    Level.objects.get(pk=pk).delete()
    return JsonResponse({'pk': pk})


def delete_house_user(request, pk):
    house_user = House.users.through.objects.filter(pk=pk).delete()
    return JsonResponse({'pk': pk})


class FlatList(UserPassesTestMixin, FormMixin, ListView):
    model = Flat
    template_name = 'admin/flat/index.html'
    form_class = FlatFilterForm

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Квартиры', user=current_user)


class FlatDetail(UserPassesTestMixin, DetailView):
    model = Flat
    template_name = 'admin/flat/detail.html'

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Квартиры', user=current_user)


@has_access(permission_page='Квартиры')
def update_flat(request, flat_id=None):
    flat = FlatData(flat_id)
    form = flat.get_form(instance=True)
    if request.method == 'POST':
        form = flat.get_form(instance=True, post=request.POST)
        if flat.save_data(request.POST) is True:
            if 'save-action-add' in request.POST:
                return redirect('admin:create_flat')
            else:
                return redirect("admin:flat_list")
    return render(request, 'admin/flat/update.html',
                  {"form": form,
                   "update": True if flat_id is not None else False})


@has_access(permission_page='Квартиры')
def delete_flat(request, pk):
    Flat.objects.get(pk=pk).delete()
    return redirect('admin:flat_list')


def get_section_level(request):
    if request.is_ajax():
        house = request.GET.get('house')
        sections = Section.objects.filter(house_id=house).values('name', 'id')
        levels = Level.objects.filter(house_id=house).values('name', 'id')
        return JsonResponse(json.dumps({'sections': list(sections), 'levels': list(levels)}), safe=False)


def get_section_flat(request):
    if request.is_ajax():
        house = request.GET.get('house')
        sections = Section.objects.filter(house_id=house).values('name', 'id')
        flats = Flat.objects.filter(house_id=house).values('number', 'id')
        return JsonResponse(json.dumps({'sections': list(sections), 'flats': list(flats)}), safe=False)


def get_flats(request):
    if request.is_ajax():
        if 'section' in request.GET.dict():
            section = request.GET.get('section')
            flats = Flat.objects.filter(section_id=section).values('number', 'id')
        else:
            level = request.GET.get('level')
            flats = Flat.objects.filter(level_id=level).values('number', 'id')
        return JsonResponse(json.dumps({'flats': list(flats)}), safe=False)


def get_flats_by_owner(request):
    if request.is_ajax():
        owner = request.GET.get('owner')
        flats = Flat.objects.filter(owner_id=owner).values('number', 'id', 'house__name')
        return JsonResponse(json.dumps({'flats': list(flats)}), safe=False)


def get_bankbooks(request):
    if request.is_ajax():
        bankbooks = BankBook.objects.filter(flat__owner_id=request.GET.get('owner')).values('id')
        return JsonResponse(json.dumps({'bankbooks': list(bankbooks)}), safe=False)


def get_owner(request):
    if request.is_ajax():
        flat = Flat.objects.get(id=request.GET.get('flat'))
        bankbook = flat.bankbook_set.first()
        owner = Owner.objects.get(id=flat.owner_id)
        try:
            response = {'id': owner.user_id, 'fullname': owner.fullname(), 'phone': owner.phone,
                        'bankbook': bankbook.id, 'tariff': flat.tariff_id}
        except AttributeError:
            response = {'id': owner.user_id, 'fullname': owner.fullname(), 'phone': owner.phone}
        return JsonResponse(json.dumps({'owner': response}), safe=False)


def get_service(request):
    if request.is_ajax():
        service = Service.objects.get(id=request.GET.get('service'))
        tariff = Tariff.objects.get(id=request.GET.get('tariff'))
        response = get_receipt_service_data(service, tariff)
        return JsonResponse(json.dumps({'service': response}), safe=False)


def get_counters(request):
    if request.is_ajax():
        counters = Counter.objects.filter(flat_id=request.GET.get('flat')).\
            values('id', 'status', 'date', 'flat__house__name', 'flat__section__name', 'flat__number',
                   'service', 'indication', 'service__unit')
        return JsonResponse({'counters': list(counters)}, safe=False)


class OwnerList(UserPassesTestMixin, FormMixin, ListView):
    model = Owner
    form_class = OwnerFilterForm
    template_name = 'admin/owner/index.html'

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Владельцы квартир', user=current_user)


class OwnerDetail(UserPassesTestMixin, DetailView):
    model = Owner
    template_name = 'admin/owner/detail.html'

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Владельцы квартир', user=current_user)


@has_access(permission_page='Владельцы квартир')
def update_owner(request, owner_id=None):
    owner = OwnerData(owner_id)
    user_form = owner.get_user_form(instance=True)
    owner_form = owner.get_owner_form(instance=True)
    if request.method == 'POST':
        user_form = owner.get_user_form(instance=True, post=request.POST)
        owner_form = owner.get_owner_form(instance=True, post=request.POST, files=request.FILES)
        if owner.save_data(request.POST, request.FILES) is True:
            return redirect("admin:owner_list")
    return render(request, 'admin/owner/update.html',
                  {"user_form": user_form,
                   "owner_form": owner_form})


@has_access(permission_page='Владельцы квартир')
def delete_owner(request, user_id):
    Owner.objects.filter(user_id=user_id).update(status=Owner.Status.disabled)
    return redirect('admin:owner_list')


class CounterView(UserPassesTestMixin, FormMixin, ListView):
    model = Counter
    template_name = 'admin/counter/index.html'
    form_class = CounterFilterForm

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Счетчики', user=current_user)

    def get_queryset(self):
        qs = super(CounterView, self).get_queryset()
        get_params = self.request.GET.dict()
        logger.info(get_params)

        if any(get_params):
            for param, value in get_params.items():
                if param != 'q' and value != '':
                    logger.info(param)
                    qs = qs.filter(**{param: value})
        return qs.distinct('flat', 'service')

    def get_form_kwargs(self):
        # use GET parameters as the data
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            kwargs.update({
                'data': self.request.GET,
            })
        return kwargs


@has_access(permission_page='Счетчики')
def update_counter(request, counter_id=None):
    counter = CounterData(counter_id)
    form = counter.get_form(instance=True)
    if request.method == 'POST':
        form = counter.get_form(instance=True, post=request.POST)
        if counter.save_data(request.POST) is True:
            if 'save-action-add' in request.POST:
                return redirect('admin:create_counter')
            else:
                return redirect("admin:counter_list")
    return render(request, 'admin/counter/update.html',
                  {"form": form,
                   "get_params": request.GET.dict(),
                   "update": True if counter_id is not None else False})


class FlatCounterList(UserPassesTestMixin, FormMixin, DetailView):
    model = Flat
    template_name = 'admin/counter/flat_counter.html'
    form_class = FlatCounterFilterForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        get_params = self.request.GET.dict()
        if any(get_params):
            context_data['counter_list'] = filter_flat_counter(self.object, get_params)
        else:
            context_data['counter_list'] = self.object.counter_set.all()
        return context_data

    def get_form_kwargs(self):
        # use GET parameters as the data
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            kwargs.update({
                'data': self.request.GET,
            })
        return kwargs

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Счетчики', user=current_user)


class CounterDetail(UserPassesTestMixin, DetailView):
    model = Counter
    template_name = 'admin/counter/detail.html'

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Счетчики', user=current_user)


class BankBookList(UserPassesTestMixin, FormMixin, StatisticMixin, ListView):
    model = BankBook
    template_name = 'admin/bank_book/index.html'
    form_class = BankBookFilterForm

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Лицевые счета', user=current_user)

    def get_queryset(self):
        qs = super(BankBookList, self).get_queryset()
        get_params = self.request.GET.dict()
        logger.info(get_params)
        if any(get_params):
            if get_params['id'] != '':
                qs = qs.filter(id__icontains=get_params['id'])
                del get_params['id']
                logger.info(get_params)
            for param, value in get_params.items():
                if param != 'q' and value != '':
                    logger.info(param)
                    qs = qs.filter(**{param: value})
        return qs

    def get_form_kwargs(self):
        # use GET parameters as the data
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            kwargs.update({
                'data': self.request.GET,
            })
        return kwargs


@has_access(permission_page='Лицевые счета')
def update_bankbook(request, bankbook_id=None):
    bankbook = BankbookData(bankbook_id)
    form = bankbook.get_form(instance=True)
    if request.method == 'POST':
        form = bankbook.get_form(instance=True, post=request.POST)
        if bankbook.save_data(request.POST) is True:
            return redirect("admin:bankbook_list")
    return render(request, 'admin/bank_book/update.html',
                  {"form": form,
                   "update": True if bankbook_id is not None else False})


class BankbookDetail(UserPassesTestMixin, DetailView):
    model = BankBook
    template_name = 'admin/bank_book/detail.html'

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Лицевые счета', user=current_user)


class CashBoxList(UserPassesTestMixin, CashBoxMixin, FormMixin, FilterMixin, StatisticMixin, ListView):
    model = CashBox
    template_name = 'admin/cash_box/index.html'
    form_class = CashBoxFilterForm

    def get_form_kwargs(self):
        # use GET parameters as the data
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            kwargs.update({
                'data': self.request.GET,
            })
        return kwargs

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Касса', user=current_user)


@has_access(permission_page='Касса')
def update_cash_box_income(request, cash_box_id=None):
    cash_box = CashBoxData(cash_box_id, CashBoxIncomeCreateForm)
    form = cash_box.get_form(instance=True, bankbook_id=request.GET.get('bankbook_id'))
    if request.method == 'POST':
        form = cash_box.get_form(instance=True, post=request.POST)
        if cash_box.save_data(request.POST) is True:
            return redirect("admin:cashbox_list")
    return render(request, 'admin/cash_box/update_income.html',
                  {"form": form,
                   "update": True if cash_box_id is not None else False})


@has_access(permission_page='Касса')
def update_cash_box_expense(request, cash_box_id=None):
    cash_box = CashBoxData(cash_box_id, CashBoxExpenseCreateForm)
    form = cash_box.get_form(instance=True)
    if request.method == 'POST':
        form = cash_box.get_form(instance=True, post=request.POST)
        if cash_box.save_data(request.POST) is True:
            return redirect("admin:cashbox_list")
    return render(request, 'admin/cash_box/update_expense.html',
                  {"form": form,
                   "update": True if cash_box_id is not None else False})


class CashBoxDetail(UserPassesTestMixin, DetailView):
    model = CashBox
    template_name = 'admin/cash_box/detail.html'

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Касса', user=current_user)


@has_access(permission_page='Касса')
def delete_cash_box(request, pk):
    CashBox.objects.get(id=pk).delete()
    return redirect('admin:cashbox_list')


class ReceiptList(UserPassesTestMixin, FormMixin, FilterMixin, StatisticMixin, ListView):
    model = Receipt
    form_class = ReceiptFilterForm
    template_name = 'admin/receipt/index.html'

    def get_form_kwargs(self, *args, **kwargs):
        # use GET parameters as the data
        kwargs = super().get_form_kwargs(*args, **kwargs)
        if self.request.method == 'GET':
            kwargs.update({
                'data': self.request.GET,
            })
        return kwargs

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Квитанции на оплату', user=current_user)


@has_access(permission_page='Квитанции на оплату')
def update_receipt(request, receipt_id=None):
    receipt = ReceiptData(receipt_id)
    form = receipt.get_form(instance=True, flat_id=request.GET.get('flat_id'))
    formset = receipt.get_formset()
    if request.method == 'POST':
        form = receipt.get_form(instance=True, post=request.POST)
        if receipt.save_data(request.POST) is True:
            return redirect("admin:receipt_list")
    return render(request, 'admin/receipt/update.html',
                  {"form": form, "formset": formset, "flat_id": request.GET.get('flat_id'),
                   "counters": receipt.get_counters(),
                   "update": True if receipt_id is not None else False})


class ReceiptDetail(UserPassesTestMixin, DetailView):
    model = Receipt
    template_name = 'admin/receipt/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ReceiptDetail, self).get_context_data(**kwargs)
        receipt = self.get_object()
        context['total'] = receipt.receiptservice_set.all().\
            aggregate(Sum('price')).get('price__sum', 0.00)
        return context

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Квитанции на оплату', user=current_user)


@has_access(permission_page='Квитанции на оплату')
def delete_receipt(request, receipt_id=None):
    if receipt_id:
        Receipt.objects.get(id=receipt_id).delete()
    else:
        logger.info(request.POST)
        Receipt.objects.filter(id__in=request.POST.getlist('ids[]')).delete()
    return redirect('admin:receipt_list')


class MasterRequestList(UserPassesTestMixin, FormMixin, FilterMixin, ListView):
    model = MasterRequest
    template_name = 'admin/master_request/index.html'
    form_class = MasterRequestFilterForm
    ordering = ['-id']

    def get_form_kwargs(self):
        # use GET parameters as the data
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            kwargs.update({
                'data': self.request.GET,
            })
        return kwargs

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Заявки вызова мастера', user=current_user)


class MasterRequestCreate(UserPassesTestMixin, CreateView):
    model = MasterRequest
    template_name = 'admin/master_request/create.html'
    form_class = MasterRequestForm
    success_url = reverse_lazy('admin:master_request_list')

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Заявки вызова мастера', user=current_user)


class MasterRequestDetail(UserPassesTestMixin, DetailView):
    model = MasterRequest
    template_name = 'admin/master_request/detail.html'

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Заявки вызова мастера', user=current_user)


@has_access(permission_page='Заявки вызова мастера')
def update_master_request(request, pk=None):
    master_request = MasterRequestData(pk)
    form = master_request.get_form(instance=True)
    if request.method == 'POST':
        form = master_request.get_form(instance=True, post=request.POST)
        if master_request.save_data(request.POST) is True:
            return redirect("admin:master_request_list")
    return render(request, 'admin/master_request/create.html',
                  {"form": form})


def delete_master_request(request, pk):
    MasterRequest.objects.get(id=pk).delete()
    return redirect('admin:master_request_list')


class MessageList(UserPassesTestMixin, ListView):
    model = Message
    template_name = 'admin/message/index.html'
    ordering = ['-id']

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Сообщения', user=current_user)


class MessageCreate(UserPassesTestMixin, CreateView):
    model = Message
    template_name = 'admin/message/create.html'
    form_class = MessageForm
    success_url = reverse_lazy('admin:message_list')

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Сообщения', user=current_user)

    def form_valid(self, form):
        form.instance.from_user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = self.request.GET.get('owner_id')
        context['owner'] = owner
        context['has_debt'] = self.request.GET.get('has_debt')
        return context


class MessageDetail(UserPassesTestMixin, DetailView):
    model = Message
    template_name = 'admin/message/detail.html'

    def test_func(self):
        current_user = User.objects.get(id=self.request.user.id)
        return has_access_for_class(permission_page='Сообщения', user=current_user)


def delete_message(request):
    logger.info(request.POST)
    Message.objects.filter(id__in=request.POST.getlist('ids[]')).delete()
    return redirect('admin:message_list')


def export_cashbox(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="cashbox.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('sheet1')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'Дата', 'Приход/расход', 'Статус', 'Статья', 'Сумма', 'Владелец квартиры', 'Лицевой счет']
    utils.write_columns(ws, columns, font_style, row_num)
    font_style = xlwt.XFStyle()

    rows = CashBox.objects.all().values_list('id', 'date', 'type', 'status', 'payment_type__name',
                                             'amount_of_money', 'bankbook__flat__owner', 'bankbook')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 6 and Owner.objects.filter(id=row[col_num]).exists():
                owner = Owner.objects.get(id=row[col_num])
                ws.write(row_num, col_num, owner.fullname(), font_style)
                col = ws.col(col_num)
                if col.width < 256 * len(owner.fullname()):
                    col.width = 256 * (len(owner.fullname()) + 5)
                continue
            elif row[col_num] is None:
                continue
            ws.write(row_num, col_num, str(row[col_num]), font_style)
            col = ws.col(col_num)
            if col.width < 256 * len(str(row[col_num])):
                col.width = 256 * (len(str(row[col_num]))+5)
    wb.save(response)
    return response


def export_bankbook(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="accounts.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('sheet1')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Лицевой счет', 'Статус', 'Дом', 'Секция', 'Квартира', 'Владелец', 'Остаток']
    utils.write_columns(ws, columns, font_style, row_num)
    font_style = xlwt.XFStyle()

    rows = BankBook.objects.all().values_list('id', 'status', 'flat__house__name', 'flat__house__section__name',
                                              'flat__number', 'flat__owner')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 5 and Owner.objects.filter(id=row[col_num]).exists():
                owner = Owner.objects.get(id=row[col_num])
                ws.write(row_num, col_num, owner.fullname(), font_style)
                col = ws.col(col_num)
                if col.width < 256 * len(owner.fullname()):
                    col.width = 256 * (len(owner.fullname()) + 5)
                continue
            elif row[col_num] is None:
                continue
            ws.write(row_num, col_num, str(row[col_num]), font_style)
            col = ws.col(col_num)
            if col.width < 256 * len(str(row[col_num])):
                col.width = 256 * (len(str(row[col_num])) + 5)
    wb.save(response)
    return response
