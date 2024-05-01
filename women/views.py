from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Women, Category, TagPost, UpLoadFiles
from .forms import AddPostForm, UploadFileForm
from django.views import View

# Меню-вкладки
menu = [
    {'title': 'О сайтище', 'url_name': 'about'},
    {'title': 'Что-то добавить', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Стать своим', 'url_name': 'login'},
]


class WomenHome(ListView):
    ''' Главнейшая страница '''
    # Привязка к модели
    # model = Women

    # Путь к шаблону. Стандартный путь <имя прилож>/<имя модели>_list.html
    # women/women_list.html (автоматич подключ).
    template_name = 'women/index.html'

    # Если, я хочу рабоать в шаблоне со своей переменной,
    # то я должен ее здесь прописать (без этого работаю с object_list)
    context_object_name = 'posts'

    # Главное меню и вкладки. extra_context-можно использовать
    # д\заранее подгото-ых данных. get-запросы не принимает!
    extra_context = {
        'title': 'Главнейшая страница',
        'menu': menu,
        'cat_selected': 0
    }

    def get_queryset(self):
        '''
        Вывожу записи со статусом Опубликована
        Привязку к модели убрать. # model = Women
        '''
        return Women.published.all().select_related('cat')


def about(request):
    '''О сайте'''
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # 'file' - птмчт в UploadFileForm так назвал
            # Создаю запись через объект модели
            fp = UpLoadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(
        request,
        'women/about.html',
        {'title': 'О сайте', 'menu': menu, 'form': form}
    )


class AddPage(View):
    '''
    Добавление статьи с помощью моей формы
    Класс в учебных целях
    '''

    def get(self, request):
        form = AddPostForm()
        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form
        }
        return render(request, 'women/addpage.html', data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            # Теперь, когда, я привязал forms к models, у меня появилась такая воз-ть сохранять
            form.save()
            return redirect('home')

        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form
        }
        return render(request, 'women/addpage.html', data)


def contact(request):
    '''Обратная связь'''
    return HttpResponse("Обратная связь")


def login(request):
    '''Авторизация'''
    return HttpResponse("Авторизация")


def show_post(request, post_slug):
    '''Отображение статьи'''
    # либо получаю одну запись, либо генерирую исключение 404
    post = get_object_or_404(Women, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,  # единица для примера
    }
    return render(request, 'women/post.html', data)


class ShowPost(DetailView):
    '''
    Детальный вывод поста
    '''
    # model = Women
    template_name = 'women/post.html'

    # По этой переменной будет выбираться статья (из маршрута)
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        '''
        Переопределяю метод get_context_data
        что бы работать с динамисес-ми данными
        '''
        # Формирую свой контекст
        context = super().get_context_data(**kwargs)

        # имя страницы
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        '''
        Что бы не выводилсь статьи со статусом Черновик по слагу
        Мы будем отбирать ту запись, котор будет отображаться ЧТО ЧТО
        '''
        # Откуда берем, по какому критерию, можно ( # model = Women)
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class WomenCategory(ListView):
    ''' Отображение катeгорий '''
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

        # имя страницы
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu

        # id-категории
        context['cat_selected'] = cat.pk
        return context


def page_not_found(request, exception):
    '''
    Обработчик (хэндлер) неправильных адресов.
    Работает при DEBUG = False
    '''
    print('[!] page_not_found')
    return HttpResponseNotFound('<h1> Куда ты тычешь!? </h1>')


def show_tag_postlist(request, tag_slug):
    '''
    Фу-я представления статей по опред тегу
    '''
    print('[!] show_tag_postlist')

    # Из модели TagPost получаю тег
    tag = get_object_or_404(TagPost, slug=tag_slug)

    '''
    Получ все статьи, котор связаны с этим тегом через объект tag, 
    через менеджер обратного сязывания related_name='tags', 
    получаю все записи связанные с данным тегом (опубликованные)
    '''
    # posts = tag.tags.filter(is_published=Women.Status.PUBLISHED)

    # утстраняю дублирующие запросы
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
    print(f'[!] tag: {tag}\nposts: {posts} ')

    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None  # Если None-синим ни чего отображаться не должно
    }
    return render(request, 'women/index.html', context=data)


class TagPostList(ListView):
    '''
    Вывод  постов по Тегам
    '''
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

        # имя страницы
        context['title'] = 'Тег: ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context
