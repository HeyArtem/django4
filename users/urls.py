from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'),
         name='password_change_done'
         ),

    # Форма с окном для ввода майла по которому восстанавливать пароль
    path('password-reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html',     # Шаблон д\отображения формы
        email_template_name="users/password_reset_email.html",   # Шаблон д\формирования текста сообщения д\электропочты
        success_url=reverse_lazy("users:password_reset_done")   # После того, как отправлено сообщение, нас перенаправят на password_reset_done
    ),
         name='password_reset'
         ),
    # Окно "Мы отправили вам по электронной почте инструкции по установке пароля..."
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
         name='password_reset_done'
         ),

    # Формирование одноразовой ссылки д\перехода на форму сброса пароля
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url=reverse_lazy("users:password_reset_complete")   # Перенаправление на password_reset_complete
         ),
            name='password_reset_confirm'
             ),

     # После сброса пароля авторизация с новой ссылкой
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'),
             name='password_reset_complete'
             ),



    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
]
