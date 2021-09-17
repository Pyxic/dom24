from django.contrib.auth.models import User

from account.forms import UserChangeForm, OwnerChangeForm
from account.models import Owner


class OwnerData:
    model = Owner
    user_form = None
    owner_form = None
    created = False

    def __init__(self, id):
        if id is None:
            self.user = User()
            self.owner = Owner()
        else:
            self.user = User.objects.get(id=id)
            self.owner, _ = Owner.objects.get_or_create(user_id=id)

    def get_user_form(self, instance=False, post=None):
        if instance is True:
            self.user_form = UserChangeForm(post, instance=self.user)
            return self.user_form
        else:
            return UserChangeForm(post)

    def get_owner_form(self, instance=False, post=None):
        if instance is True:
            self.owner_form = OwnerChangeForm(post, instance=self.owner, prefix='owner')
            return self.owner_form
        else:
            return OwnerChangeForm(post)

    def save_data(self, post, files):
        user_form = UserChangeForm(post, instance=self.user)
        owner_form = OwnerChangeForm(post, files, instance=self.owner, prefix='owner')
        print(owner_form.errors)
        if user_form.is_valid() and owner_form.is_valid():
            updated_user = user_form.save(commit=False)
            if 'password' in user_form.changed_data:
                updated_user.set_password(user_form.cleaned_data['password'])
            updated_user.save()
            updated_profile = owner_form.save(commit=False)
            updated_profile.user_id = updated_user.id
            updated_profile.save()
            return True
        else:
            return False
