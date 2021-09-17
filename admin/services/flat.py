from admin.forms import FlatCreateForm
from admin.models import Flat


class FlatData:
    model = Flat
    form = None
    created = False

    def __init__(self, id):
        if id is None:
            self.object = self.model()
            self.created = True
        else:
            self.object = self.model.objects.get(id=id)

    def get_form(self, instance=False, post=None):
        if instance is True:
            self.form = FlatCreateForm(post, instance=self.object)
            return self.form
        else:
            return FlatCreateForm(post)

    def save_data(self, post):
        if self.created:
            form = FlatCreateForm(post)
        else:
            form = FlatCreateForm(post, instance=self.object)
        if form.is_valid():
            form.save()
            return True
        else:
            return False
