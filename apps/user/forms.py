from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from apps.user.models import User


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'role', 'is_active', 'name', 'gender', 'age', 'occupation', 'village', 'taluka', 'district', 'state', 'pin_code', 'mobile_number_1', 'mobile_number_2', 'profile_picture')


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'role', 'is_active', 'name', 'gender', 'age', 'occupation', 'village', 'taluka', 'district', 'state', 'pin_code', 'mobile_number_1', 'mobile_number_2', 'profile_picture')

    password = None
    # password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        request_present = False
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
            request_present = True
        super(UserChangeForm, self).__init__(*args, **kwargs)
        # IF not user is NOT Manager, remove fields from form.
        if request_present:
            if not ( 3 == self.request.user.role ):
                self.fields.pop('role')
                self.fields.pop('is_active')


class UserUpdatePasswordForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username',)

    # password = None
    password = forms.CharField(widget=forms.PasswordInput())

