from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from sitewomen import settings
from women.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),
    path('users/', include('users.urls', namespace='users')),
    path("__debug__/", include("debug_toolbar.urls")),  # django-toolbar
    path('social-auth/', include('social_django.urls', namespace='social')),    # Авторицация через соц.сети
]

# В коллекцию urlpatterns добавляю префикс MEDIA_URL и этот префикс связываю
# с маршрутом MEDIA_ROOT который ведет на каталог media (! только DEBUG = True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обработчик (хэндлер) неправильных адресов
# если DEBUG = False
handler404 = page_not_found

# Замена заголовков в админ панели
admin.site.site_header = '💈️ Кастомная Панель администрирования'
admin.site.index_title = 'Известные женщины мира'
