from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    '''
        Скомбинированный вариант.class LoginUserForm(AuthenticationForm)+class Meta:
        class LoginUserForm(AuthenticationForm)-делает стили для формы
        class Meta-возвращает текущую модель
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

class RegisterUserForm(forms.ModelForm):
    '''
        Форма д\регистрации пользователя (для registe.html)
        forms.ModelForm (т.к. при рес-ции поль-ля, будет добавляться новЗапись в БД, форма должна быть связана с моделью)
        инфа по полям: https://docs.djangoproject.com/en/4.2/topics/auth/default/
    '''
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())

    class Meta:
        '''
            class Meta - т.к. эта форма связана с моделью
            labels - метки д\полей
        '''
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

    def clean_password2(self):
        '''
            Валидация, проверка совпадения введеных паролей.
        '''
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password']

    def clean_email(self):
        '''
            Валидация, проверка, есть ли в БД пользователь с таким майлом
        '''
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой E-mail уже существует!')
        return email

