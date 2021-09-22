import json

from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.forms import modelformset_factory
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.utils.dateparse import postgres_interval_re
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView, ListView, CreateView, UpdateView, DetailView
from django.views.generic.edit import FormMixin

from account.forms import UserChangeForm, ProfileChangeForm
from account.models import Profile, Owner
from admin.forms import SeoCreateForm, GalleryForm, FlatFilterForm, CounterFilterForm, FlatCounterFilterForm, \
    BankBookFilterForm, CashBoxFilterForm, CashBoxIncomeCreateForm, CashBoxExpenseCreateForm
from admin.models import SeoText, Gallery, Document, Service, Unit, Tariff, Requisites, PaymentItem, House, Flat, \
    Section, Level, Counter, BankBook, CashBox
from admin.services.bankbook import BankbookData
from admin.services.cashbox import CashBoxMixin, CashBoxData
from admin.services.counter import CounterData, filter_flat_counter
from admin.services.flat import FlatData
from admin.services.house import HouseData
from admin.services.owner import OwnerData
from admin.services.services import UnitData, ServiceData, TariffData
from admin.services.singleton_pages import get_singleton_page_data, RequisitesPageData


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'admin/statistic.html')


def singleton_page(request, page_name):
    singleton_data = get_singleton_page_data(page_name)
    if request.method == 'POST':
        singleton_data.save_data(request.POST, request.FILES)
        return redirect(f"admin:{page_name}", page_name)
    return render(request, singleton_data.render_url, singleton_data.get_content())


def delete_from_gallery(request, image_id):
    Gallery.objects.get(id=image_id).delete()
    return JsonResponse({'image_id': image_id})


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


def delete_document(request, pk):
    Document.objects.get(pk=pk).delete()
    return JsonResponse({'pk': pk})


@require_POST
def delete_service(request):
    pk = request.POST.get('pk')
    Service.objects.get(pk=pk).delete()
    return JsonResponse({'pk': pk})


@require_POST
def delete_unit(request):
    pk = request.POST.get('pk')
    Unit.objects.get(pk=pk).delete()
    return JsonResponse({'pk': pk})


class TariffList(ListView):
    model = Tariff
    template_name = 'admin/settings/tariff/index.html'


def update_tariff(request, tariff_id=None):
    tariff = TariffData(tariff_id)
    form = tariff.get_form(instance=True)
    formset = tariff.get_formset()
    if request.method == 'POST':
        if tariff.save_data(request.POST) is True:
            return redirect("admin:tariff_list")
    return render(request, 'admin/settings/tariff/update.html',
                  {"form": form,
                   "formset": formset})


def delete_tariff(request, tariff_id):
    Tariff.objects.get(id=tariff_id).delete()
    return redirect('admin:tariff_list')


def get_unit_by_service(request):
    if request.is_ajax():
        unit = Service.objects.get(id=request.GET.get('id')).unit_id
        return HttpResponse(unit)


def settings_roles(request):
    roles = Group.objects.all()
    return render(request, 'admin/settings/roles.html',{
        'roles': roles
    })


class UserList(ListView):
    model = User
    template_name = 'admin/settings/user/index.html'


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


def delete_user(request, user_id):
    User.objects.get(id=user_id).delete()
    return redirect('admin:user_list')


def settings_requisites(request):
    requisites_data = RequisitesPageData()
    if request.method == 'POST':
        requisites_data.save_data(request.POST)
        return redirect(f"admin:requisites")
    return render(request, requisites_data.render_url, requisites_data.get_content())


class PaymentItemList(ListView):
    model = PaymentItem
    template_name = 'admin/settings/payment_item/index.html'


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


class HouseList(ListView):
    model = House
    template_name = 'admin/house/house/index.html'


class HouseDetail(DetailView):
    model = House
    template_name = 'admin/house/house/detail.html'


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


class FlatList(FormMixin, ListView):
    model = Flat
    template_name = 'admin/flat/index.html'
    form_class = FlatFilterForm


class FlatDetail(DetailView):
    model = Flat
    template_name = 'admin/flat/detail.html'


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
        section = request.GET.get('section')
        flats = Flat.objects.filter(section_id=section).values('number', 'id')
        return JsonResponse(json.dumps({'flats': list(flats)}), safe=False)


def get_bankbooks(request):
    if request.is_ajax():
        bankbooks = BankBook.objects.filter(flat__owner_id=request.GET.get('owner')).values('id')
        return JsonResponse(json.dumps({'bankbooks': list(bankbooks)}), safe=False)


def get_owner(request):
    if request.is_ajax():
        flat = Flat.objects.get(id=request.GET.get('flat'))
        owner = Owner.objects.get(id=flat.owner_id)
        response = {'id': owner.user_id, 'fullname': owner.fullname(), 'phone': owner.phone}
        return JsonResponse(json.dumps({'owner': response}), safe=False)


class OwnerList(ListView):
    model = Owner
    template_name = 'admin/owner/index.html'


class OwnerDetail(DetailView):
    model = Owner
    template_name = 'admin/owner/detail.html'


def update_owner(request, owner_id=None):
    owner = OwnerData(owner_id)
    user_form = owner.get_user_form(instance=True)
    owner_form = owner.get_owner_form(instance=True)
    if request.method == 'POST':
        user_form = owner.get_user_form(instance=True, post=request.POST)
        owner_form = owner.get_owner_form(instance=True, post=request.POST)
        if owner.save_data(request.POST, request.FILES) is True:
            return redirect("admin:owner_list")
    return render(request, 'admin/owner/update.html',
                  {"user_form": user_form,
                   "owner_form": owner_form})


def delete_owner(request, user_id):
    Owner.objects.get(user_id=user_id).delete()
    return redirect('admin:owner_list')


class CounterView(FormMixin, ListView):
    model = Counter
    template_name = 'admin/counter/index.html'
    form_class = CounterFilterForm

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


def update_counter(request, counter_id=None):
    counter = CounterData(counter_id)
    form = counter.get_form(instance=True)
    if request.method == 'POST':
        form = counter.get_form(instance=True, post=request.POST)
        if counter.save_data(request.POST) is True:
            return redirect("admin:counter_list")
    return render(request, 'admin/counter/update.html',
                  {"form": form,
                   "update": True if counter_id is not None else False})


class FlatCounterList(FormMixin, DetailView):
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


class CounterDetail(DetailView):
    model = Counter
    template_name = 'admin/counter/detail.html'


class BankBookList(FormMixin, ListView):
    model = BankBook
    template_name = 'admin/bank_book/index.html'
    form_class = BankBookFilterForm

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


class BankbookDetail(DetailView):
    model = BankBook
    template_name = 'admin/bank_book/detail.html'


class CashBoxList(CashBoxMixin, FormMixin, ListView):
    model = CashBox
    template_name = 'admin/cash_box/index.html'
    form_class = CashBoxFilterForm


def update_cash_box_income(request, cash_box_id=None):
    cash_box = CashBoxData(cash_box_id, CashBoxIncomeCreateForm)
    form = cash_box.get_form(instance=True)
    if request.method == 'POST':
        form = cash_box.get_form(instance=True, post=request.POST)
        if cash_box.save_data(request.POST) is True:
            return redirect("admin:cashbox_list")
    return render(request, 'admin/cash_box/update_income.html',
                  {"form": form,
                   "update": True if cash_box_id is not None else False})


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


def delete_cash_box(request, pk):
    CashBox.objects.get(id=pk).delete()
    return redirect('admin:cashbox_list')
