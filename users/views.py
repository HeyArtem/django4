from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.urls import reverse, reverse_lazy
from .forms import LoginUserForm


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


# def login_user(request):
#     if request.method == 'POST':
#         # В таком случае форму заполняю данными из request.POST
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             # Аутентификация Проверка, что пользователь есть в БД
#             user = authenticate(request, username=cd['username'],
#                                 password=cd['password'])
#             # Проверка, что oн активный
#             if user and user.is_active:
#                 # Авторизирую
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('home'))
#     # Если метод GET
#     else:
#         form = LoginUserForm()
#
#     return render(request, 'users/login.html', {'form': form})


# def logout_user(request):
#     logout(request)
#     # потому что пространство имен (namespace='users') переводит нас на приложение users
#     return HttpResponseRedirect(reverse('users:login'))
