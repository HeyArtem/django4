from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from .models import Women, Category, TagPost, UpLoadFiles
from .forms import AddPostForm, UploadFileForm
from django.views import View
from .utils import DataMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class WomenHome(DataMixin, ListView):
    '''
    Главнейшая страница.
    Добавляю mixin
    '''
    print('[!] class WomenHome(ListView)')
    # Привязка к модели
    # model = Women

    # Путь к шаблону. Стандартный путь <имя прилож>/<имя модели>_list.html
    # women/women_list.html (автоматич подключ).
    template_name = 'women/index.html'

    # Если, я хочу рабоать в шаблоне со своей переменной,
    # то я должен ее здесь прописать (без этого работаю с object_list)
    context_object_name = 'posts'
    title_page = 'Главнейшая страница'
    cat_selected = 0

    # Пагинация. Когда используется ListView, то автоматически в шаблон
    # передаются переменные paginator & page_obj
    # paginate_by = 3

    def get_queryset(self):
        print('[!] get_queryset from class WomenHome(DataMixin, ListView)')
        '''
        Вывожу записи со статусом Опубликована
        Привязку к модели убрать. # model = Women
        '''
        return Women.published.all().select_related('cat')




@login_required
def about(request):
    '''
        О сайте
        I Var:
        @login_required - доступна, только зареганым (работает в связке с LOGIN_URL(settings))

        II Var:
        @login_required(login_url='/admin/')-здесь мой адрес перенаправления (это более высокий прио-тет, чем LOGIN_URL)
    '''
    print('[!] def about(request)')
    contact_list = Women.published.all().select_related('cat')
    paginator = Paginator(contact_list, 3)

    # GET-запрос из которого я получаю номер текущей страницы
    page_number = request.GET.get('page')
    # Получаю текущую страницу по номеру (page_number)
    page_obj = paginator.get_page(page_number)

    # if request.method == 'POST':
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         # 'file' - птмчт в UploadFileForm так назвал.
    #         # Создаю запись через объект модели
    #         fp = UpLoadFiles(file=form.cleaned_data['file'])
    #         fp.save()
    # else:
    #     form = UploadFileForm()
    return render(
        request,
        'women/about.html',
        {'title': 'О сайте', 'page_obj': page_obj}
    )


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    '''
    Добавление статьи. Автоматизированное представление html-формы.
    Передает в шаблон переменную form.
    Добавляю mixin.
    '''
    print('[!] class AddPage(CreateView)')
    # Класс формы (без вызова)
    form_class = AddPostForm

    # Имя шаблона
    template_name = 'women/addpage.html'
    title_page = 'Добавление статьи'

    # URL на который будет перенаправление после успешной отправки данных
    # reverse - возвращает полный маршрут, но при запуске кода, будет ошибка, тк маршрут 'home'не существует на момент определения AddPage-класса
    # reverse_lazy - потому, что она будет выполняться, когда придет ее очередь (ее можно всегда вызывать за место reverse)
    success_url = reverse_lazy('home')

    # URL адрес на который перевести неавторизованного пользователя работает в связке с LoginRequiredMixin
    # login_url = '/admin/'


class UpdatePage(DataMixin, UpdateView):
    ''' Изменение существ-их записей) '''
    print('[!] class UpdatePage(UpdateView)')
    model = Women
    fields = ['title', 'content', 'photo', 'cat', 'is_published', ]

    # Имя шаблона
    template_name = 'women/addpage.html'

    # URL на который будет перенаправление после успешной отправки данных
    # reverse - возвращает полный маршрут, но при запуске кода, будет ошибка, тк маршрут 'home'не существует на момент определения AddPage-класса
    # reverse_lazy - потому, что она будет выполняться, когда придет ее очередь (ее можно всегда вызывать за место reverse)
    success_url = reverse_lazy('home')
    title_page = 'Редачу статейку'


def contact(request):
    '''Обратная связь'''
    print('[!] def contact(request)')
    return HttpResponse("Обратная связь")


def login(request):
    '''Авторизация'''
    print('[!] def login(request)')
    return HttpResponse("Авторизация")


class ShowPost(DataMixin, DetailView):
    print('[!] class ShowPost(DataMixin, DetailView)')
    '''
    Наполнение шаблона информацией.
    Использую Mixin
    (пишется на I месте, создам его в women/utils.py)
    '''
    template_name = 'women/post.html'

    # По этой переменной будет выбираться статья (из маршрута)
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        print('[!] get_context_data in ShowPost')
        '''
        Переопределяю метод get_context_data
        что бы работать с динамисес-ми данными
        '''
        # Формирую свой контекст
        context = super().get_context_data(**kwargs)

        # get_mixin_context- я создал в women/utils.py
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        print('[!] get_object in ShowPost')
        '''
        Что бы не выводилсь статьи со статусом Черновик по слагу
        Мы будем отбирать ту запись, котор будет отображаться ЧТО ЧТО
        '''
        # Откуда берем, по какому критерию, можно ( # model = Women)
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class WomenCategory(DataMixin, ListView):
    ''' Отображение катeгорий '''
    print('[!] class WomenCategory(ListView)')
    # Путь к шаблону.
    template_name = 'women/index.html'

    # Переменная, котор буду передавать в контексте
    context_object_name = 'posts'

    # Если несуществующий слаг-404
    allow_empty = False


    def get_queryset(self):
        '''
        Вывожу записи с опред слагом. В этом случае не делаю привязку к модели
        'cat_slug' - потому что в url так назвал
        '''
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        '''
        Переопределяю метод get_context_data
        что бы работать с динамисес-ми данными
        '''
        # Формирую свой контекст
        context = super().get_context_data(**kwargs)

        # Название категории
        cat = context['posts'][0].cat
        return self.get_mixin_context(
            context,
            title='Категория - ' + cat.name,
            cat_selected=cat.pk,
        )


def page_not_found(request, exception):
    '''
    Обработчик (хэндлер) неправильных адресов.
    Работает при DEBUG = False
    '''
    print('[!] def page_not_found(request, exception)')
    return HttpResponseNotFound('<h1> Куда ты тычешь!? </h1>')


class TagPostList(DataMixin, ListView):
    ''' Вывод постов по Тегам '''
    print('[!] class TagPostList(ListView)')
    # Путь к шаблону.
    template_name = 'women/index.html'

    # Переменная, котор буду передавать в контексте
    context_object_name = 'posts'

    # Если несуществующий Тэг-404
    allow_empty = False

    def get_queryset(self):
        '''
        Хочу сформировать кверисет постов по опред слагу.
        Переопределяем метод get_queryset попутно сохраняя объект TagPost,
        используя полученный в kwargs'ах tag_slug (из маршрута).
        Этот queryset хранит коллекцию из всех объектов Women, которые связаны
        с этим тегом.
        '''
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        '''
        Переопределяем метод get_context_data, сначала вызвав его из
        родительского класса и сохранив в переменную context.
        Далее добавляем в наш словарь 'context' еще несколько ключ-значений,
        '''

        context = super().get_context_data(**kwargs)

        # Название тега
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(
            context,
            title='Тег: ' + tag.tag,
        )


class DeletePage(DeleteView):
    ''' Удаление статьи '''
    print('[!] class DeletePage(DeleteView)')

    # Привязка к модели
    model = Women

    # Переменная, котор буду передавать в контексте
    context_object_name = 'posts'

    # Шаблон удаления
    template_name = 'women/delete.html'

    # Переадресация после удаления
    success_url = reverse_lazy('home')

    # Если несуществующий Тэг-404
    allow_empty = False
