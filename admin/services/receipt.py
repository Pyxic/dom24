from django.db import models
from django.forms import inlineformset_factory

from admin.forms import ReceiptCreateForm, ReceiptServiceForm
from admin.models import Receipt, ReceiptService, Service, Tariff, TariffService, Counter, Flat
from django.core.exceptions import ObjectDoesNotExist
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ReceiptData:
    model = Receipt
    form = None
    formset = None
    created = False

    def __init__(self, id):
        if id is None:
            self.object = self.model()
            self.created = True
        else:
            self.object = self.model.objects.get(id=id)

    def get_form(self, instance=False, post=None, flat_id=None):
        if instance is True:
            if self.created:
                if flat_id:
                    flat = Flat.objects.get(id=flat_id)
                    self.form = ReceiptCreateForm(post, instance=self.object,
                                                  initial={'house': flat.house_id,
                                                           'section': flat.section_id,
                                                           'flat': flat.id})
                else:
                    self.form = ReceiptCreateForm(post, instance=self.object)
            else:
                self.form = ReceiptCreateForm(post, instance=self.object,
                                              initial={'house': self.object.flat.house_id if self.object.flat else None,
                                              'section': self.object.flat.section_id if self.object.flat else None})
            return self.form
        else:
            return ReceiptCreateForm(post)

    def get_counters(self):
        if self.created:
            return Counter.objects.all()
        else:
            return Counter.objects.filter(flat_id=self.object.flat_id)

    def get_formset(self):
        self.formset = inlineformset_factory(self.model, ReceiptService, form=ReceiptServiceForm, extra=0)
        return self.formset(instance=self.object)

    def save_data(self, post):
        if self.created:
            form = ReceiptCreateForm(post)
        else:
            form = ReceiptCreateForm(post, instance=self.object)
        logger.info(form.errors)
        if form.is_valid():
            created = form.save(commit=False)
            formset = self.formset(post, instance=created)
            logger.info(formset.errors)
            if formset.is_valid():
                created.save()
                formset.save()
                return True
        else:
            return False


def get_receipt_service_data(service: Service, tariff: Tariff):
    unit = service.unit_id
    try:
        unit_price = service.tariffservice_set.get(tariff_id=tariff.id).price
    except TariffService.DoesNotExist:
        unit_price = None
    return {'unit': unit, 'unit_price': unit_price}
