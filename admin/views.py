from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.forms import modelformset_factory
from django.shortcuts import render, redirect

# Create your views here.
from admin.forms import SeoCreateForm, GalleryForm
from admin.models import SeoText, Gallery
from admin.services.singleton_pages import get_singleton_page_data


def index(request):
    return render(request, 'admin/statistic.html')


def singleton_page(request, page_name):
    singleton_data = get_singleton_page_data(page_name)
    if request.method == 'POST':
        singleton_data.save_data(request.POST, request.FILES)
        return redirect(f"admin:{page_name}", page_name)
    return render(request, singleton_data.render_url, singleton_data.get_content())
