from django.forms import modelformset_factory, inlineformset_factory
from django.shortcuts import redirect

from admin.forms import UnitForm, ServiceForm, TariffCreateForm, TariffServiceForm
from admin.models import Unit, Service, Tariff, TariffService


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

    def __init__(self, tariff_id):
        if tariff_id is None:
            self.tariff = Tariff()
            self.created = True
        else:
            self.tariff = Tariff.objects.get(id=tariff_id)

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
            created.save()
            formset = self.formset(post, instance=created)
            if formset.is_valid():
                formset.save()
                return True
            else:
                return False
