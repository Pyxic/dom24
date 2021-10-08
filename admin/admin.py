from django.contrib import admin
from import_export import resources
from .models import CashBox

# Register your models here.


class CashBoxResource(resources.ModelResource):

    class Meta:
        model = CashBox
        fields = ('id', 'date', 'type', 'status', 'payment_type', 'amount_of_money', 'bankbook__flat__owner',
                  'bankbook')
