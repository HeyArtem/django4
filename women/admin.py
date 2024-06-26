from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Women, Category


class MarriedFilter(admin.SimpleListFilter):
    '''
    Для фильтра по статусу.
    Указать в list_filter
    Возвращает: url:.../status=married
    '''
    title = 'Статус женщин'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        '''
        Возвращает возможные значения
        параметра статус.
        '''
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    # Поля, котор будут отображаться в форме
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'husband', 'tags', 'author']
    # exclude = ['tags', 'is_published']  # Антипод fields (исключить поля)

    # Поля только для чтения
    readonly_fields = ['post_photo']

    # Автоматич формирование slug (только с отключенным readonly_fields)
    prepopulated_fields = {'slug': ('title',)}

    # Улучшенный ввод тегов
    filter_horizontal = ['tags']
    # filter_vertical = ['tags']

    # ДопПоля в админке с женщинами
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat', 'author')

    # Кликабельность полей д\редактирования (не должно быть в list_editable)
    list_display_links = ('title',)

    # Поля сортировки в админке
    ordering = ['-time_create', 'title']

    # Редактирование строки, не открывая карточки (костыль в модели)
    # list_editable = ('is_published',  'title', 'cat')
    list_editable = ('is_published',)

    # Пагинация
    list_per_page = 5

    # Доп ф-я опубликовать/в черновик, в разделе действия
    actions = ['set_published', 'set_draft']

    # Поля поиска. 'cat__name'-поиск по категориям (вспомни люкапы, title__startswith)
    search_fields = ['title', 'cat__name']

    # Панель фильтрации справа
    list_filter = [MarriedFilter, 'cat__name', 'is_published']

    # Кнопка "Сохранить" вверху и внизу страницы редактирования поста
    save_on_top = True

    @admin.display(description='Изображение', ordering='content')
    def post_photo(self, women: Women):
        '''
        Вычисляемое поле, для вывода миниатюры фото в админке
        рядом с постом. Возвращает html-строку.
        mark_safe - что бы html-теги не экранировались
        Прописать в list_display, fields, readonly_fields
        '''
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return 'Без фото'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        '''
        Доп функция в разделе действия
        request - объект запроса
        queryset - выбранные записи
        Прописвть в actions
        message_user - сообщение пользователю о кол-ве измененных записей
        '''
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей.')

    @admin.action(description='Снять с публикации')
    def set_draft(self, request, queryset):
        '''
        Доп функция в разделе действия
        messages.WARNING - специальный формат отображения изменения
        '''
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f'{count} записей снято с публикации.', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Поля в админке
    list_display = ('id', 'name')

    # Кликабельность полей д\редактирования
    list_display_links = ('id', 'name')
