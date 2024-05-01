from django import forms
from .models import Category, Husband, Women
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


class AddPostForm(forms.ModelForm):
    '''
    Простецкий вар формы. Поля лучше называть, как в модели.
    С валидатором clean_title
    '''

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

    class Meta:
        '''
        Появятся все поля, кроме автоматических (дата создания и обновления)
        '''
        model = Women
        # fields = '__all__'
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'husband', 'cat', 'tags', ]

        # Виджет для title & content
        widgets = {
           'title': forms.TextInput(attrs={'class': 'form-input'}),
           'content': forms.Textarea(attrs={'cols': 60,  'rows': 5}),
        }

        # Меняю имя для слага
        labels = {'slug': 'URL'}

    # Валидатор для title
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title

class UploadFileForm(forms.Form):
    '''
    Определил класс формы для загрузки файла
    Форма (не привязана к модели - forms.Form)
    '''
    # file = forms.FileField(label='Фаил')
    file = forms.ImageField(label='Фаил')
