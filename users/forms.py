from datetime import datetime
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class LoginUserForm(AuthenticationForm):
    '''
        Скомбинированный вариант.class LoginUserForm(AuthenticationForm)+class Meta:
        class LoginUserForm(AuthenticationForm)-делает стили для формы
        class Meta-возвращает текущую модель
        widget=forms.TextInput(attrs={...}) - стили
    '''
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    class Meta:
        '''
            get_user_model - возвращает текущую модель пользователя
            так рекомендуется, потому что я могу прописать свою моdель,
            тогда фу-я будет использовать ее.
        '''
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    '''
        Форма д\регистрации пользователя (для register.html)
        forms.ModelForm (т.к. при рес-ции поль-ля, будет добавляться новЗапись в БД, форма должна быть связана с моделью)
        инфа по полям: https://docs.djangoproject.com/en/4.2/topics/auth/default/
        widget=forms.TextInput(attrs={...}) - стили
    '''
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    password2 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    class Meta:
        '''
            class Meta - т.к. эта форма связана с моделью
            labels - метки д\полей
        '''
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        # Стили
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_email(self):
        '''
            Валидация, проверка, есть ли в БД пользователь с таким майлом
        '''
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой E-mail уже существует!')
        return email

class ProfileUserForm(forms.ModelForm):
    '''
        Форма д\отображения, пользовательского профайла.
    '''
    username = forms.CharField(
        disabled=True,  # Невозможно редактировать
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    email = forms.CharField(
        disabled=True,
        label='E-mail',
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    this_year = datetime.now().year
    date_birth = forms.DateField(label="Дата рождения", widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))))
    class Meta:
        '''
            class Meta - т.к. эта форма связана с моделью
            labels - метки д\полей
        '''
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'date_birth', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя343434',
            'last_name': 'Фамилия',
        }
        # Стили
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }
class UserPasswordChangeForm(PasswordChangeForm):
    '''
        Класс д\отображения формы смены пароля.
    '''
    old_password = forms.CharField(
        label='Старый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    new_password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
