from django.contrib import admin
from django.urls import path, include
from women.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),
    path("__debug__/", include("debug_toolbar.urls")),  # django-toolbar
]

# Обработчик (хэндлер) неправильных адресов
# если DEBUG = False
handler404 = page_not_found

# Замена заголовков в админ панели
admin.site.site_header = '💈️ Кастомная Панель администрирования'
admin.site.index_title = 'Известные женщины мира'
