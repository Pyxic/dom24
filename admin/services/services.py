from django.forms import modelformset_factory, inlineformset_factory
from django.shortcuts import redirect

from account.forms import PermissionAccessForm
from account.models import Profile, PermissionPage, PermissionAccess
from admin.forms import UnitForm, ServiceForm, TariffCreateForm, TariffServiceForm
from admin.models import Unit, Service, Tariff, TariffService
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UnitData:
    model = Unit
    model_formset = None
    form = UnitForm

    def get_formset(self, post=None):
        self.model_formset = modelformset_factory(self.model, self.form, extra=0)
        return self.model_formset(post)


class ServiceData:
    model = Service
    model_formset = None
    form = ServiceForm
    prefix = 'service'

    def get_formset(self, post=None):
        self.model_formset = modelformset_factory(self.model, self.form, extra=0)
        return self.model_formset(post, prefix=self.prefix)


class TariffData:
    model = Tariff
    form = None
    formset = None
    created = False
    clone = False

    def __init__(self, tariff_id, clone):
        if tariff_id is None:
            self.tariff = Tariff()
            self.created = True
        else:
            self.tariff = Tariff.objects.get(id=tariff_id)
            self.clone = clone

    def get_form(self, instance=False):
        if instance is True:
            self.form = TariffCreateForm(instance=self.tariff)
            return self.form
        else:
            return TariffCreateForm()

    def get_formset(self):
        self.formset = inlineformset_factory(self.model, TariffService, form=TariffServiceForm, extra=0)
        return self.formset(instance=self.tariff)

    def save_data(self, post):
        if self.created:
            form = TariffCreateForm(post)
        else:
            form = TariffCreateForm(post, instance=self.tariff)
        if form.is_valid():
            created = form.save(commit=False)
            if self.clone is True:
                created.pk = None
            created.save()
            formset = self.formset(post, instance=created)
            if formset.is_valid():
                if self.clone:
                    for f in formset.forms:
                        instance = f.save(commit=False)
                        instance.tariff = created
                        instance.save()
                else:
                    formset.save()
                return True
            else:
                return False


def get_roles_form(post=None):
    form = {}
    pages = PermissionPage.objects.all()
    logger.info(pages)
    exist_permissions = PermissionAccess.objects.all().count()
    for role in Profile.Role.values:
        logger.info(role)
        form[role] = []
        exist_permissions = PermissionAccess.objects.filter(role=role).order_by('page')
        if exist_permissions.count() > 0:
            for exist_permission in exist_permissions:
                if post:
                    form[role] += [PermissionAccessForm(post, instance=exist_permission,
                                                        prefix=str(role) + str(exist_permission.page))]
                else:
                    form[role] += [
                        PermissionAccessForm(instance=exist_permission, prefix=str(role) + str(exist_permission.page))]
        else:
            for page in pages:
                if post:
                    form[role] += [PermissionAccessForm(post, prefix=str(role) + str(page))]
                else:
                    form[role] += [PermissionAccessForm(initial={'role': role, 'page': page}, prefix=str(role)+str(page))]
    logger.info(form)
    return form

