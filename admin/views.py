from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.forms import modelformset_factory
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.utils.dateparse import postgres_interval_re
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView, ListView, CreateView, UpdateView

from account.forms import UserChangeForm, ProfileChangeForm
from account.models import Profile
from admin.forms import SeoCreateForm, GalleryForm
from admin.models import SeoText, Gallery, Document, Service, Unit, Tariff, Requisites, PaymentItem, House
from admin.services.services import UnitData, ServiceData, TariffData
from admin.services.singleton_pages import get_singleton_page_data, RequisitesPageData


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
                print('yes')
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


def update_house(request, house_id=None):
    house = HouseData(house_id)
    form = house.get_form(instance=True)
    #formset = tariff.get_formset()
    if request.method == 'POST':
        if house.save_data(request.POST) is True:
            return redirect("admin:tariff_list")
    return render(request, 'admin/settings/tariff/update.html',
                  {"form": form,
                   })
