from django.db.models import Sum
from django.views.generic.list import MultipleObjectMixin

from admin.forms import CashBoxIncomeCreateForm
from admin.models import CashBox
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class CashBoxMixin(MultipleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_income = CashBox.objects.filter(status=True, type='приход').\
            aggregate(Sum('amount_of_money')).get('amount_of_money__sum', 0.00)
        total_expenses = CashBox.objects.filter(status=True, type='расход').\
            aggregate(Sum('amount_of_money')).get('amount_of_money__sum', 0.00)
        context['total_income'] = total_income if total_income else 0
        context['total_expenses'] = total_expenses if total_expenses else 0
        return context


class CashBoxData:
    model = CashBox
    form = None
    created = False

    def __init__(self, id, form_model):
        if id is None:
            self.object = self.model()
            self.created = True
        else:
            self.object = self.model.objects.get(id=id)
        self.form_model = form_model

    def get_form(self, instance=False, post=None):
        if instance is True:
            if self.created:
                self.form = self.form_model(post, instance=self.object)
            else:
                self.form = self.form_model(post, instance=self.object,
                                            initial={'owner': self.object.bankbook.flat.owner_id if self.object.bankbook else None})
            return self.form
        else:
            return self.form_model(post)

    def save_data(self, post):
        if self.created:
            form = self.form_model(post)
        else:
            form = self.form_model(post, instance=self.object)
        logger.info(form.errors)
        if form.is_valid():
            form.save()
            return True
        else:
            return False
