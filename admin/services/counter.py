from admin.forms import CounterCreateForm
from admin.models import Counter


class CounterData:
    model = Counter
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
                self.form = CounterCreateForm(post, instance=self.object)
            else:
                self.form = CounterCreateForm(post, instance=self.object,
                                              initial={'house': self.object.flat.house_id,
                                                       'section': self.object.flat.section_id})
            return self.form
        else:
            return CounterCreateForm(post)

    def save_data(self, post):
        if self.created:
            form = CounterCreateForm(post)
        else:
            form = CounterCreateForm(post, instance=self.object)
        if form.is_valid():
            form.save()
            return True
        else:
            return False


def filter_flat_counter(flat, params):
    counters = Counter.objects.filter(
        flat=flat
    )
    if 'date' in params and params['date'] != '':
        date_range = params['date'].split(' - ')
        counters = counters.filter(date__range=date_range)
    params.pop('date', None)
    for param, value in params.items():
        if param != 'q' and value != '':
            counters = counters.filter(**{param: value})
    return counters
