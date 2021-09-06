from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

# Create your views here.
from admin.models import Gallery, MainPage, ContactPage, NearBlock, AboutUs, Document, ServicePage, CustomerService


def main_page(request):
    main_page = MainPage.objects.first()
    near = NearBlock.objects.all()
    contacts = ContactPage.objects.first()
    page_content_type = ContentType.objects.get_for_model(main_page)
    gallery = Gallery.objects.filter(content_type__pk=page_content_type.id, object_id=main_page.id)
    return render(request, 'main/pages/main_page.html', {
        "main_page": main_page,
        "gallery": gallery,
        "contact": contacts,
        "near": near,
        # "today": format_date(date.today(), 'M MMMM', locale='ru_RU')
    })


def about_us(request):
    page = AboutUs.objects.first()
    page_content_type = ContentType.objects.get_for_model(page)
    gallery_main = Gallery.objects.filter(content_type__pk=page_content_type.id, object_id=page.id, is_additional=False)
    gallery_additional = Gallery.objects.filter(content_type__pk=page_content_type.id, object_id=page.id, is_additional=True)
    documents = Document.objects.all()
    return render(request, 'main/pages/about_us_page.html', {
        "page": page,
        "gallery_main": gallery_main,
        "gallery_additional": gallery_additional,
        "documents": documents,
    })


def services(request):
    page = ServicePage.objects.first()
    services = CustomerService.objects.all()
    return render(request, 'main/pages/service_page.html', {
        "page": page,
        "services": services,
    })


def contacts(request):
    page = ContactPage.objects.first()
    return render(request, 'main/pages/contact_page.html', {
        "page": page
    })
