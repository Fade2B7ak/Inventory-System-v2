from django import forms
from django.forms import ModelForm
from .models import NewProduct
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class AddProductsForm(ModelForm):
    class Meta:
        model = NewProduct
        fields = ['itemClass', 'name', 'model', 'quantity', 'price_per_piece', 'ready_to_load']


class UpdateProductForm(ModelForm):
    class Meta:
        model = NewProduct
        fields = ['itemClass', 'name', 'model', 'quantity', 'price_per_piece', 'ready_to_load']
