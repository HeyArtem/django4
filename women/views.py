from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.template.loader import render_to_string
from .models import Women, Category, TagPost
from .forms import AddPostForm

# Меню-шапка
menu = [
    {'title': 'О сайтище', 'url_name': 'about'},
    {'title': 'Что-то добавить', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Стать своим', 'url_name': 'login'},
]


def index(request):
    '''
    Главнейшая страница
    'cat_selected' - Подсветка категрии
    '''
    # Предыдущий менеджер
    # posts = Women.objects.filter(is_published=1)

    # Новый менеджер (свой)
    # posts = Women.published.all()

    # утстраняю дублирующие запросы
    posts = Women.published.all().select_related('cat')

    data = {
        'title': 'Главнейшая страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0
    }
    return render(request, 'women/index.html', context=data)


def about(request):
    '''О сайте'''
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu})


def addpage(request):
    '''
    Добавление статьи с помощью моей формы
    '''
    if request.method =='POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            try:
                Women.objects.create(**form.cleaned_data)
                
                # После успешного добавления статьи, перенаправляю на index
                return redirect('home')
            except:
                # В форму передаю сообщение об ошибке
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddPostForm()
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


def show_category(request, cat_slug):
    '''
    Отображение катгорий
    'cat_selected' - Подсветка категoрии
    '''
    category = get_object_or_404(Category, slug=cat_slug)
    # posts = Women.published.filter(cat_id=category.pk)

    # утстраняю дублирующие запросы
    posts = Women.published.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'women/index.html', context=data)


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
