from django import forms

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(
        label='Адрес доставки',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Улица, дом, квартира, индекс'
        }),
        max_length=500,
        required=True
    )
    phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (999) 123-45-67'
        }),
        max_length=20,
        required=True
    )
    comments = forms.CharField(
        label='Комментарии к заказу',
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'form-control',
            'placeholder': 'Дополнительные пожелания'
        }),
        required=False
    )