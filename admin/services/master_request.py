from admin.forms import MasterRequestForm
from admin.models import MasterRequest


class MasterRequestData:
    model = MasterRequest
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
            if self.created:
                self.form = MasterRequestForm(post, instance=self.object)
            else:
                self.form = MasterRequestForm(post, instance=self.object,
                                               initial={'owner': self.object.flat.owner_id})
            return self.form
        else:
            return MasterRequestForm(post)

    def save_data(self, post):
        if self.created:
            form = MasterRequestForm(post)
        else:
            form = MasterRequestForm(post, instance=self.object)
        if form.is_valid():
            form.save()
            return True
        else:
            return False
