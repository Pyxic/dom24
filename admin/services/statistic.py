import datetime
import json
import math

from django.db.models import Sum
from django.views.generic.list import MultipleObjectMixin

from account.models import Owner
from admin.models import House, MasterRequest, Flat, BankBook, CashBox


class StatisticData:

    def __init__(self):
        self.house_count = House.objects.all().count()
        self.owner_count = Owner.objects.filter(status='активен').count()
        self.master_request_in_process_count = MasterRequest.objects.filter(status='в процессе').count()
        self.flat_count = Flat.objects.all().count()
        self.bankbook_count = BankBook.objects.all().count()
        self.master_request_new_count = MasterRequest.objects.filter(status='новое').count()
        self.incomes_expenses = self.get_incomes_expenses()
        self.sum_account_debts = sum(get_account_debts())
        self.sum_account_balance = sum(get_account_balance())
        self.state_cashbox = get_state_cashbox()

    def get_incomes_expenses(self):
        current_year = datetime.datetime.now().year
        labels = ['Янв.,', 'Фев.,', 'Мар.,', 'Апр.,', 'Май,', 'Июн.,', 'Июл.,', 'Авг.,', 'Сен.,', 'Окт.,', 'Нояб.,', 'Дек.,']
        labels = [label + str(current_year) for label in labels]
        data_incomes = []
        data_expenses = []
        for i in range(12):
            expenses = str(CashBox.objects.filter(type='расход', date__month=i+1).aggregate(Sum('amount_of_money'))\
                .get('amount_of_money__sum'))
            incomes = str(CashBox.objects.filter(type='приход', date__month=i+1).aggregate(Sum('amount_of_money')) \
                .get('amount_of_money__sum'))
            data_incomes.append(incomes)
            data_expenses.append(expenses)
        return {"labels": labels, "incomes": data_incomes, "expenses": data_expenses}


def get_account_debts():
    balances = []
    for bankbook in BankBook.objects.filter(status='Активен'):
        if bankbook.balance() < 0:
            balances.append(math.fabs(bankbook.balance()))
    return balances


def get_account_balance():
    balances = []
    for bankbook in BankBook.objects.filter(status='Активен'):
        if bankbook.balance() > 0:
            balances.append(math.fabs(bankbook.balance()))
    return balances


def get_state_cashbox():
    expenses = str(CashBox.objects.filter(type='расход').aggregate(Sum('amount_of_money')) \
                   .get('amount_of_money__sum'))
    incomes = str(CashBox.objects.filter(type='приход').aggregate(Sum('amount_of_money')) \
                  .get('amount_of_money__sum'))
    try:
        return float(incomes) - float(expenses)
    except ValueError:
        return None


class StatisticMixin(MultipleObjectMixin):

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StatisticMixin, self).get_context_data(**kwargs)
        context['account_debts'] = sum(get_account_debts())
        context['account_balance'] = sum(get_account_balance())
        context['state_cashbox'] = get_state_cashbox()
        return context
