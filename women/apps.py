from django.apps import AppConfig


class WomenConfig(AppConfig):
    # Изменил заголовок 'WOMEN' в панели
    verbose_name = 'Женщины мира 🗺️'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'women'
