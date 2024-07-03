from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.urls import reverse, reverse_lazy
from .forms import LoginUserForm, RegisterUserForm


class LoginUser(LoginView):
    '''
        Регистрация пользователя.
        LoginUserForm - моя форма, за место стандартной AuthenticationForm.
    '''
    # form_class = AuthenticationForm
    form_class = LoginUserForm  # Моя форма из forms.py
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    # def get_success_url(self):
    #     '''
    #         Перевод пользователя, после авторизации на главную страницу.
    #         Есть аналог: LOGIN_REDIRECT_URL = 'home'(в settings)
    #     '''
    #     return reverse_lazy('home')


def register(request):
    '''
        Фу-я представления для регистрации пользователя
    '''
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            '''
                Если метод передачи POST, 
                создаю форму с данными, котор были переданы,
                проверяю, что все поля заполнены верно,
                создаю объект user, но не заношу в БД,
                шифрую пароль (метод set_password) и заношу его в атрибут 'password',
                записываю в БД
             
            '''
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'users/register_done.html')
    else:
        '''
        Если GET-запрос, формирую пустую форму и отображаю на register.html
        '''
        form = RegisterUserForm()
    return render(request, 'users/register.html', {'form': form})
