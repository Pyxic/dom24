from django.forms import inlineformset_factory

from admin.forms import HouseCreateForm, SectionForm, LevelForm, HouseUserForm
from admin.models import House, Section, Level


class HouseData:
    model = House
    form = None
    section_formset = None
    level_formset = None
    user_formset = None
    created = False

    def __init__(self, house_id):
        if house_id is None:
            self.object = House()
            self.created = True
        else:
            self.object = House.objects.get(id=house_id)

    def get_form(self, instance=False):
        if instance is True:
            self.form = HouseCreateForm(instance=self.object)
            return self.form
        else:
            return HouseCreateForm()

    def get_section_formset(self):
        self.section_formset = inlineformset_factory(self.model, Section, form=SectionForm, extra=0)
        return self.section_formset(instance=self.object, prefix='section')

    def get_level_formset(self):
        self.level_formset = inlineformset_factory(self.model, Level, form=LevelForm, extra=0)
        return self.level_formset(instance=self.object, prefix='level')

    def get_user_formset(self):
        self.user_formset = inlineformset_factory(self.model, House.users.through, form=HouseUserForm, extra=0)
        return self.user_formset(instance=self.object, prefix='user')

    def save_data(self, post, files):
        if self.created:
            form = HouseCreateForm(post, files)
        else:
            form = HouseCreateForm(post, files, instance=self.object)
        if form.is_valid():
            created = form.save(commit=False)
            created.save()
            section_formset = self.section_formset(post, instance=created, prefix='section')
            level_formset = self.level_formset(post, instance=created, prefix='level')
            user_formset = self.user_formset(post, instance=created, prefix='user')
            if section_formset.is_valid() and level_formset.is_valid() and user_formset.is_valid():
                section_formset.save()
                level_formset.save()
                user_formset.save()
                return True
            else:
                return False
