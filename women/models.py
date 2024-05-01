from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


# def translit_to_eng(s: str) -> str:
#     '''
#     Для save. Костыль для создания slug
#     '''
#     d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
#          'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
#          'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
#          'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
#          'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}
#
#     return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class PublishedManager(models.Manager):
    '''
    Это менеджер, который будет возвращать только опубликованные
    статьи.
    '''

    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    class Status(models.IntegerChoices):
        '''
        Что-бы статус выводился форме, при заполнении
        и для понятности PublishedManager (1 или 0 малопонятно)
        '''
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='Слаг',
        validators=[
            MinLengthValidator(5, message="Минимум 5 символов"),
            MaxLengthValidator(100, message="Максимум 100 символов"),
        ]
    )
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        default=None,
        blank=True,
        null=True,  # Нулевое знач допустимо (нужно во время миграций, наверно, что бы конфликта небыло тк там есть уже)
        verbose_name='Фото'
    )
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время редактирования')
    # is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT, verbose_name='Статус')

    # Это костыль, т.к. я настроил list_editable в админке, а BooleanField не позволяет корректно отображать
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.DRAFT,
        verbose_name='Статус'
    )
    cat = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='posts',
        verbose_name='Категория'
    )  # 'Category' строка, тк создана после этого класса
    tags = models.ManyToManyField(
        'TagPost',
        blank=True,
        related_name='tags',
        verbose_name='Теги'
    )
    husband = models.OneToOneField(
        'Husband',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='women',
        verbose_name='Муж'
    )

    # Что бы после создания нового менеджера PublishedManager,
    # работал предыдущий менеджер objects
    objects = models.Manager()

    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        # меняю название приложения 'Womens'в админке
        verbose_name = '✨️ Известные женщины'
        verbose_name_plural = '✨️ Известные женщины'
        # По умолчанию сортировка по -time_create
        ordering = ['-time_create']
        # Поля котор я индексирую
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        '''
        Формирует url-адрес д\кажд конкретн записи
        напр: /category/aktrisy/
        Так же, это кнопка "Смотреть на сайте" в разделе
        http://127.0.0.1:8000/admin/women/women/ЛюбаяЖенщина/change/
        '''
        return reverse('post', kwargs={'post_slug': self.slug})

    # def save(self, *args, **kwargs):
    #     '''
    #     Автоматическое формирование слага. Вар 1 (Костыль).
    #     '''
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(*args, *kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        # Замена в админке 'Categorys'
        verbose_name = '⚜️ Категория'
        verbose_name_plural = '⚜️ Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        '''
        Формирует url-адрес д\кажд конкретн записи
        post_slug - передаю этот параметр (см urls)
        '''
        res = reverse('category', kwargs={'cat_slug': self.slug})
        print(f"[!] ф-я get_absolute_url in Category: {res}")
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name

class UpLoadFiles(models.Model):
    '''
    Модель новой таблицы,
    в которой будут храниться ссылки на загруженные файлы
    '''
    file = models.FileField(upload_to='uploads_model')
