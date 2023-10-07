from django.forms import ModelForm, TextInput, DateInput, NumberInput, Select, EmailInput, HiddenInput
from .models import Order, UserData, BalanceOperations
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['explanation', 'cost', 'category', 'deadline']
        labels = {
            "explanation": "",
            "cost": "",
            "category": "",
            "deadline": "",
        }
        widgets = {
            "explanation": TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Описание сути заказа'
            }),
            "cost": NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Стоимость'
            }),
            "category": Select(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Выберите категорию'
            }),
            "deadline": DateInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Дедлайн', 'type': 'text',
                'onfocus': "(this.type='date')"
            }),
        }



class UserDataForm(ModelForm):
    class Meta:
        model = UserData
        fields = ['last_name', 'first_name', 'mail', 'bank_account', 'role', 'about']
        widgets = {
            "last_name": TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Фамилия'
            }),
            "first_name": TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Имя'
            }),
            "mail": EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Email-адрес'
            }),
            "bank_account": NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Номер банковской карты'
            }),
            "role": Select(
                attrs={
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Статус'
                }),
            "about": TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Подробнее о вас'
            }),
        }


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'password': TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Пароль'
            }),
            'username': TextInput(
                attrs={
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Имя пользователя'
                }
            )
        }


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'password': TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Пароль'
            }),
            'username': TextInput(
                attrs={
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Имя пользователя'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AddOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['degree_to_company'].empty_label = 'Нет оценки'
        self.fields['degree_to_performer'].empty_label = 'Нет оценки'
        self.fields['category'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Order
        fields = '__all__'


class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['performer', 'degree_to_company', 'degree_to_performer', 'in_work', 'done']

#Никитина форма
class WorkReadyForm(forms.Form):
    work_form = forms.CharField(max_length=200, label='Ваш ответ', required=False)
    degree = forms.ChoiceField(choices=((1, 'Очень плохо'), (2, "Плохо"), (3, "Средне"), (4, "Хорошо"), (5, "Отлично")),
                               required=False)

class BalanceForm(forms.ModelForm):
    class Meta:
        model = BalanceOperations
        fields = ['type_operation', 'summa']
        labels = {
            "type_operation": "Тип операции",
            "summa": "Сумма"
        }
        widgets = {
            'type_operation': Select(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Тип операции'
            }),
            'summa': TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Сумма'
            }),
        }

