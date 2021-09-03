from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import DeleteView

from admin.forms import SeoCreateForm, GalleryForm
from admin.models import SeoText, Gallery, Document
from admin.services.singleton_pages import get_singleton_page_data


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


def delete_document(request, pk):
    Document.objects.get(pk=pk).delete()
    return JsonResponse({'pk': pk})
