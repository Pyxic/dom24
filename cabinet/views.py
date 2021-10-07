from os import path

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, CreateView
from wkhtmltopdf.views import PDFTemplateView

from account.models import Owner
from admin.forms import ReceiptFilterForm, MasterRequestForm
from admin.models import BankBook, Flat, Receipt, TariffService, Message, MasterRequest, Requisites
from admin.services.cashbox import FilterMixin
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from cabinet.services.utils import fetch_pdf_resources, link_callback
from dom24 import settings


@login_required
def index(request):
    return render(request, 'cabinet/index.html')


@login_required
def summary(request, flat_id):
    flat = Flat.objects.get(id=flat_id)
    return render(request, 'cabinet/summary.html', {'flat': flat})


class ReceiptList(LoginRequiredMixin, FormMixin, FilterMixin, ListView):
    model = Receipt
    form_class = ReceiptFilterForm
    template_name = 'cabinet/receipt/index.html'

    def get_form_kwargs(self, *args, **kwargs):
        # use GET parameters as the data
        kwargs = super().get_form_kwargs(*args, **kwargs)
        if self.request.method == 'GET':
            kwargs.update({
                'data': self.request.GET,
            })
        return kwargs


class ReceiptDetail(LoginRequiredMixin, DetailView):
    model = Receipt
    template_name = 'cabinet/receipt/detail.html'


class FlatServiceDetail(LoginRequiredMixin, DetailView):
    model = Flat
    template_name = 'cabinet/tariff/index.html'


class MessageList(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'cabinet/message/index.html'


class MessageDetail(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'cabinet/message/detail.html'


class MasterRequestList(LoginRequiredMixin, ListView):
    model = MasterRequest
    template_name = 'cabinet/master_request/index.html'
    ordering = ['-id']

    def get_queryset(self):
        qs = super(MasterRequestList, self).get_queryset()
        user = User.objects.get(id=self.request.user.id)
        qs = qs.filter(flat__owner=user.owner)
        return qs


class MasterRequestCreate(LoginRequiredMixin, CreateView):
    model = MasterRequest
    template_name = 'cabinet/master_request/create.html'
    form_class = MasterRequestForm
    success_url = reverse_lazy('cabinet:master_request_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = Owner.objects.get(user_id=self.request.user.id)
        context['owner'] = owner.id
        return context


@login_required
def delete_master_request(request, pk):
    MasterRequest.objects.get(id=pk).delete()
    return redirect('cabinet:master_request_list')


class OwnerProfile(LoginRequiredMixin, View):

    def get(self, request):
        owner = Owner.objects.get(user_id=request.user.id)
        return render(request, 'cabinet/owner/index.html', {'owner': owner})


def render_pdf_view(request, receipt_id):
    template_path = 'cabinet/receipt/pdf.html'
    requisites = Requisites.objects.first()
    receipt = Receipt.objects.get(id=receipt_id)
    # print(receipt.flat.owner.user.first_name)
    context = {'requisites': requisites.information,
               'static': settings.STATIC_ROOT,
               'receipt': receipt}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html.encode('UTF-8'), dest=response, encoding='utf-8')
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


class MyPDF(PDFTemplateView):
    filename = 'my_pdf.pdf'
    template_name = '/cabinet/receipt/pdf.html'
    requisites = Requisites.objects.first()
    context = {'requisites': requisites.information}
    cmd_options = {
        'margin-top': 3,
    }
