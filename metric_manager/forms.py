from .models import FitbitUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
class MyRegistrationForm(UserCreationForm):
    #email = forms.EmailField(required=True)
    #name = forms.CharField(required=True)

    class Meta:
        model = FitbitUser
        fields = {'username', 'password1', 'password2'}

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
        # user.email = self.cleaned_data['email']
        # user.name = self.cleaned_data['name']

        if commit:
            user.save()

        return user
