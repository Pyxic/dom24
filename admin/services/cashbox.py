from django.db.models import Sum
from django.views.generic.list import MultipleObjectMixin

from admin.forms import CashBoxIncomeCreateForm
from admin.models import CashBox, BankBook
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


class FilterMixin(MultipleObjectMixin):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        get_params = self.request.GET.dict()
        logger.info(get_params)
        if any(get_params):
            if 'date_range' in get_params and get_params['date_range'] != '':
                date_range = get_params['date_range'].split(' - ')
                qs = qs.filter(date__range=date_range)
            get_params.pop('date_range', None)
            for param, value in get_params.items():
                if param != 'q' and value != '':
                    logger.info(param)
                    qs = qs.filter(**{param: value})
        return qs

    def get_form_kwargs(self, *args, **kwargs):
        # use GET parameters as the data
        kwargs = super().get_form_kwargs(*args, **kwargs)
        if self.request.method == 'GET':
            kwargs.update({
                'data': self.request.GET,
            })
        return kwargs


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

    def get_form(self, instance=False, post=None, bankbook_id=None):
        if instance is True:
            if self.created:
                if bankbook_id:
                    bankbook = BankBook.objects.get(id=bankbook_id)
                    self.form = self.form_model(post, instance=self.object,
                                                initial={'owner': bankbook.flat.owner_id,
                                                         'bankbook': bankbook_id})
                else:
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
