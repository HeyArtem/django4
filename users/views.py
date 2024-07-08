from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm


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


class RegisterUser(CreateView):
    '''
        Класс представления для регистрации пользователя
    '''
    form_class = RegisterUserForm   # Моя форма из forms.py
    template_name = 'users/register.html'  # Шаблон котор использую
    extra_context = {'title': 'Регистрация111'}
    success_url = reverse_lazy('users:login')   # Маршрут куда перенаправить пользователя, после успешной регистрации

class ProfileUser(LoginRequiredMixin, UpdateView):
    '''
        Класс д\представления формы профайла
        Наследуюсь от:
            LoginRequiredMixin-т.к. профаил могут просматривать только авторизованные пользователи
            UpdateView-базовый класс, отвечает за изменение текущих записей
    '''
    model = get_user_model()
    form_class = ProfileUserForm   # Моя форма из forms.py
    template_name = 'users/profile.html'     # Шаблон
    extra_context = {'title': 'Профиль пользователя'}

    def get_success_url(self):
        '''
            Метод, что бы джанго знал, куда перенаправляться
            если я какие-то поля поменяю и сохраню
        '''
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        '''
            Метод выводит запись, которая будет отображаться и редактироваться.
            Потому что до этого, в urls, я выводил в профайле пользователя
            по 'profile/<int:pk>/' и это позволяло пользователю просматривать
            профайлы других поль-ей
        '''
        return self.request.user


