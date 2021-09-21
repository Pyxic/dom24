from admin.forms import BankbookCreateForm
from admin.models import BankBook


class BankbookData:
    model = BankBook
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
                self.form = BankbookCreateForm(post, instance=self.object)
            else:
                self.form = BankbookCreateForm(post, instance=self.object,
                                               initial={'house': self.object.flat.house_id,
                                                        'section': self.object.flat.section_id})
            return self.form
        else:
            return BankbookCreateForm(post)

    def save_data(self, post):
        if self.created:
            form = BankbookCreateForm(post)
        else:
            form = BankbookCreateForm(post, instance=self.object)
        if form.is_valid():
            form.save()
            return True
        else:
            return False
