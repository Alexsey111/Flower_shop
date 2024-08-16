from django import forms
from allauth.account.forms import SignupForm
from .models import Category, DeliveryMethod, PaymentMethod, Order, Profile, Review

class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=30, label='Name')
    phone = forms.CharField(max_length=15, label='Phone')
    address = forms.CharField(widget=forms.Textarea, label='Address')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data.get('name')
        user.save()

        # Создаем или обновляем профиль
        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone = self.cleaned_data.get('phone')
        profile.address = self.cleaned_data.get('address')
        profile.save()

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


class CheckoutForm(forms.ModelForm):
    delivery_option = forms.ChoiceField(
        choices=Order.DELIVERY_CHOICES,
        required=True,
        label="Выберите способ доставки"
    )
    payment_option = forms.ChoiceField(
        choices=Order.PAYMENT_CHOICES,
        required=True,
        label="Выберите способ оплаты"
    )

    class Meta:
        model = Order
        fields = ['delivery_option', 'payment_option']


class OrderPreviewForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_option', 'payment_option']



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_option', 'payment_option']
        widgets = {
            'delivery_option': forms.Select(choices=Order.DELIVERY_CHOICES),
            'payment_option': forms.Select(choices=Order.PAYMENT_CHOICES),
        }

class ConfirmLogoutForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='Ваш пароль')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review', 'rating']
        widgets = {
            'review': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Напишите ваш отзыв...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
        labels = {
            'review': 'Отзыв',
            'rating': 'Оценка',
        }
