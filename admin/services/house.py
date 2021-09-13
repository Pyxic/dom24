from admin.models import House


class HouseData:
    model = House
    form = None
    formset = None
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

    # def get_formset(self):
    #     self.formset = inlineformset_factory(self.model, TariffService, form=TariffServiceForm, extra=0)
    #     return self.formset(instance=self.tariff)

    # def save_data(self, post):
    #     if self.created:
    #         form = TariffCreateForm(post)
    #     else:
    #         form = TariffCreateForm(post, instance=self.tariff)
    #     if form.is_valid():
    #         created = form.save(commit=False)
    #         created.save()
    #         formset = self.formset(post, instance=created)
    #         if formset.is_valid():
    #             formset.save()
    #             return True
    #         else:
    #             return False
