from django import forms


class OrderForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=20)

