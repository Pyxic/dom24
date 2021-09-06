from django.forms import modelformset_factory

from admin.forms import UnitForm
from admin.models import Unit


class UnitData:
    model = Unit
    model_formset = None
    form = UnitForm

    def get_formset(self, post=None):
        self.model_formset = modelformset_factory(self.model, self.form, extra=3)
        return self.model_formset(post=post)
