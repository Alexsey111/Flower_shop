from django import forms
from allauth.account.forms import SignupForm
from .models import Category

class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=30, label='Name')
    phone = forms.CharField(max_length=15, label='Phone')
    address = forms.CharField(widget=forms.Textarea, label='Address')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data.get('name')
        user.profile.phone = self.cleaned_data.get('phone')
        user.profile.address = self.cleaned_data.get('address')
        user.save()
        return user


class ProductFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Выберите категорию"
    )
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Минимальная цена'})
    )
    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Максимальная цена'})
    )
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Поиск по названию'})
    )
