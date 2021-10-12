from __future__ import annotations
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.forms import inlineformset_factory, modelformset_factory, ModelForm
from django.shortcuts import redirect

from admin.forms import MainConfForm, AboutUsConfForm, ServicePageConfForm, ContactPageConfForm, GalleryForm, \
    SeoCreateForm, CustomerServiceForm, DocumentForm, NearBlockForm, RequisitesForm
from admin.models import MainPage, AboutUs, ServicePage, ContactPage, Gallery, SeoText, CustomerService, Document, \
    NearBlock, Requisites
from abc import ABC, abstractmethod

from admin.singleton import SingletonModel


def get_singleton_page_data(page_name: str) -> SingletonData:
    pages = {
        'main_page': MainPageData,
        'about_us_page': AboutUsData,
        'service_page': ServicePageData,
        'contact_page': ContactData,
    }
    return pages[page_name]()


class SingletonData(ABC):
    model = SingletonModel
    form_model = ModelForm
    form = None
    model_formset = None
    formset = None
    page = None
    seo_form = None

    def is_instance(self):
        if self.model.objects.all().count() == 1:
            return True
        return False

    def save_data(self, post, files):
        form = self.form_model(post, files, instance=self.page)
        formset = self.model_formset(post, files,
                                     instance=self.page)
        if SeoText.objects.filter(id=self.page.seo_id).exists():
            seo_form = SeoCreateForm(post, prefix="seo", instance=SeoText.objects.get(id=self.page.seo_id))
        else:
            seo_form = SeoCreateForm(post, prefix="seo")
        if form.is_valid() and seo_form.is_valid() and formset.is_valid():
            seo_instance = seo_form.save()
            created_page = form.save(commit=False)
            created_page.seo_id = seo_instance.id
            created_page.save()
            formset.save()

    @abstractmethod
    def get_content(self):
        pass


class MainPageData(SingletonData):
    model = MainPage
    form_model = MainConfForm
    render_url = 'admin/pages/main_page.html'
    extra = 3
    formset_type = generic_inlineformset_factory

    def __init__(self):
        if self.is_instance():
            self.page = self.model.objects.first()
            self.seo_form = SeoCreateForm(prefix="seo", instance=SeoText.objects.get(id=self.page.seo_id))
        else:
            self.page = self.model()
            self.seo_form = SeoCreateForm(prefix="seo")
        self.form = self.form_model(instance=self.page)
        self.model_formset = generic_inlineformset_factory(Gallery, form=GalleryForm, extra=self.extra, max_num=3)
        self.formset = self.model_formset(instance=self.page)
        self.near_model_formset = modelformset_factory(NearBlock, form=NearBlockForm, extra=6, max_num=6)
        self.near_formset = self.near_model_formset(prefix='near')

    def is_instance(self):
        if self.model.objects.all().count() == 1:
            return True
        return False

    def generate_formset(self):
        return self.model_formset

    def get_content(self):
        return {
            "form": self.form,
            "seo_form": self.seo_form,
            "formset": self.formset,
            "near_formset": self.near_formset,
        }

    def save_data(self, post, files):
        form = self.form_model(post, files, instance=self.page)
        formset = self.model_formset(post, files,
                                     instance=self.page)
        near_formset = self.near_model_formset(post, files, prefix='near')
        if SeoText.objects.filter(id=self.page.seo_id).exists():
            seo_form = SeoCreateForm(post, prefix="seo", instance=SeoText.objects.get(id=self.page.seo_id))
        else:
            seo_form = SeoCreateForm(post, prefix="seo")
        if form.is_valid() and seo_form.is_valid() and formset.is_valid() and near_formset.is_valid():
            seo_instance = seo_form.save()
            created_page = form.save(commit=False)
            created_page.seo_id = seo_instance.id
            created_page.save()
            formset.save()
            near_formset.save()


class AboutUsData(SingletonData):
    model = AboutUs
    form_model = AboutUsConfForm
    form = None
    render_url = 'admin/pages/about_us.html'
    extra = 0
    formset_type = generic_inlineformset_factory
    model_formset = None
    formset = None
    page = None
    seo_form = None

    def __init__(self):
        if self.is_instance():
            self.page = self.model.objects.first()
            self.seo_form = SeoCreateForm(prefix="seo", instance=SeoText.objects.get(id=self.page.seo_id))
        else:
            self.page = self.model()
            self.seo_form = SeoCreateForm(prefix="seo")
        self.form = self.form_model(instance=self.page)
        self.model_formset = generic_inlineformset_factory(Gallery, form=GalleryForm, extra=self.extra)
        self.formset = self.model_formset(instance=self.page)
        self.doc_model_formset = modelformset_factory(Document, form=DocumentForm, extra=0)
        self.doc_formset = self.doc_model_formset(prefix='doc')

    def get_content(self):
        return {
            "form": self.form,
            "seo_form": self.seo_form,
            "formset": self.formset,
            "doc_formset": self.doc_formset,
        }

    def save_data(self, post, files):
        form = self.form_model(post, files, instance=self.page)
        formset = self.model_formset(post, files,
                                     instance=self.page)
        doc_formset = self.doc_model_formset(post, files, prefix='doc')
        if SeoText.objects.filter(id=self.page.seo_id).exists():
            seo_form = SeoCreateForm(post, prefix="seo", instance=SeoText.objects.get(id=self.page.seo_id))
        else:
            seo_form = SeoCreateForm(post, prefix="seo")
        if form.is_valid() and seo_form.is_valid() and formset.is_valid() and doc_formset.is_valid():
            seo_instance = seo_form.save()
            created_page = form.save(commit=False)
            created_page.seo_id = seo_instance.id
            created_page.save()
            formset.save()
            doc_formset.save()


class ServicePageData(SingletonData):
    model = ServicePage
    form_model = ServicePageConfForm
    render_url = 'admin/pages/service.html'
    extra = 3
    formset_type = modelformset_factory

    def __init__(self):
        if self.is_instance():
            self.page = self.model.objects.first()
            self.seo_form = SeoCreateForm(prefix="seo", instance=SeoText.objects.get(id=self.page.seo_id))
        else:
            self.page = self.model()
            self.seo_form = SeoCreateForm(prefix="seo")
        self.model_formset = modelformset_factory(CustomerService, form=CustomerServiceForm, extra=self.extra)
        self.formset = self.model_formset()

    def save_data(self, post, files):
        formset = self.model_formset(post, files)
        if SeoText.objects.filter(id=self.page.seo_id).exists():
            seo_form = SeoCreateForm(post, prefix="seo", instance=SeoText.objects.get(id=self.page.seo_id))
        else:
            seo_form = SeoCreateForm(post, prefix="seo")
        if seo_form.is_valid() and formset.is_valid():
            seo_instance = seo_form.save()
            self.page.seo_id = seo_instance.id
            self.page.save()
            formset.save()

    def get_content(self):
        return {
            "seo_form": self.seo_form,
            "formset": self.formset,
        }


class ContactData(SingletonData):
    model = ContactPage
    form_model = ContactPageConfForm
    render_url = 'admin/pages/contact.html'
    extra = 0
    formset_type = None

    def __init__(self):
        if self.is_instance():
            self.page = self.model.objects.first()
            self.seo_form = SeoCreateForm(prefix="seo", instance=SeoText.objects.get(id=self.page.seo_id))
        else:
            self.page = self.model()
            self.seo_form = SeoCreateForm(prefix="seo")
        self.form = self.form_model(instance=self.page)

    def save_data(self, post, files):
        form = self.form_model(post, instance=self.page)
        if SeoText.objects.filter(id=self.page.seo_id).exists():
            seo_form = SeoCreateForm(post, prefix="seo", instance=SeoText.objects.get(id=self.page.seo_id))
        else:
            seo_form = SeoCreateForm(post, prefix="seo")
        if form.is_valid() and seo_form.is_valid():
            seo_instance = seo_form.save()
            created_page = form.save(commit=False)
            created_page.seo_id = seo_instance.id
            created_page.save()

    def get_content(self):
        return {
            "seo_form": self.seo_form,
            "form": self.form,
        }


class RequisitesPageData(SingletonData):
    model = Requisites
    form_model = RequisitesForm
    render_url = 'admin/settings/requisites.html'

    def __init__(self):
        if self.is_instance():
            self.page = self.model.objects.first()
        else:
            self.page = self.model()
        self.form = self.form_model(instance=self.page)

    def save_data(self, post):
        form = self.form_model(post, instance=self.page)
        if form.is_valid():
            form.save()

    def get_content(self):
        return {
            "form": self.form,
        }

