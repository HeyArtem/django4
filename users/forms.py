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
