from django import forms
from .models import Category, Husband
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class RussianValidator:
    '''
    Рукописный валидатор
    ALLOWED_CHARS - допустимые символы
    code - (название)
    '''
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None):
        '''
        Если сюда передается какое-то сообщение,
        то оно и будет использовано,
        а по умолчанию --> else
        '''
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value, *args, **kwargs):
        '''
        __call__ - вызывается, когда срабатывает валидатор
        Проверяем, что если, хотя бы один символ, не соответствует
        разрешенным (ALLOWED_CHARS), то эта проверка срабатывает.
        Генерируется исключение, передается сообщение и код
        '''
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.Form):
    '''
    Простецкий вар формы. Поля лучше называть, как в модели.
    С валидатором clean_title
    '''
    title = forms.CharField(
        # min_length=5,
        max_length=255,
        label='Заголовок',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        # validators=[
        #     RussianValidator()
        # ],
        validators=[
            MinLengthValidator(5, message="Нужно 5 символов"),
            MaxLengthValidator(100, message="Максимум 100 символов"),
        ],
    )
    slug = forms.SlugField(
        # max_length=255,
        label='URL',
        validators=[
            MinLengthValidator(5, message="Минимум 5 forms символов"),
            MaxLengthValidator(100, message="Максимум 100 символов"),
        ]
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'colls': 50, 'rows': 5}),
        required=False,
        label='Контент'
    )  # required- не обязательный для заполнения
    is_published = forms.BooleanField(
        required=False,
        initial=True,
        label='Статус'
    )  # initial=True - по умолчанию, уже галочка в форме
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label='Категория не выбрана',
        label='Категория'
    )
    husband = forms.ModelChoiceField(
        queryset=Husband.objects.all(),
        empty_label='Не замужем',
        required=False,
        label='Муж'
    )

    def clean_title(self):
        '''
        Простой валидатор для title
        naming - clean_NameField
        '''
        title = self.cleaned_data['title']
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "

        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны присутствовать только русские символы, дефис и пробел.")
        return title