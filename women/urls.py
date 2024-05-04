from django.urls import path, re_path, register_converter
from . import views, converters

# Регаю конвертер
register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.WomenHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),  # Добавление статьи
    path('contact/', views.contact, name='contact'),  # Контакты
    path('login/', views.login, name='login'),  # Войти
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
    # Удаление
    path('delete/<slug:slug>/', views.DeletePage.as_view(), name='delete_page'),
]
