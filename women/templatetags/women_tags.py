from django import template
from django.db.models import Count
import women.views as views
from women.models import Category, TagPost

register = template.Library()


# @register.simple_tag(name='getcats')
# def get_categories():
#     '''
#     Простой тег. Будет возвращать категории для наших постов
#     могу восполь-ся в любом шаблоне проекта
#     name='getcats' - имя по которому буду вызывать
#     '''
#     return views.cats_db


# @register.inclusion_tag('women/list_categories.html')
# def show_categories():
#     '''
#     Включающий тег, позволяет дополнительено формировать
#     свой собсьвенный шаблон на основе некоторых пользовательских данных
#     и возвращать фрагмент html-страницы
#     '''
#     cats = views.cats_db
#     return {'cats': cats}


@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
    '''
    Включающий тег, позволяет дополнительено формировать
    свой собственный шаблон на основе некоторых пользовательских данных
    и возвращать фрагмент html-страницы.
    Добавил cat_selected=0 - Подсветка при наведении
    '''
    # cats = Category.objects.all()

    # Чтобы сайт баре не отображались категории у которых нет постов.
    cats = Category.objects.annotate(total=Count('posts')).filter(total__gt=0)

    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('women/list_tags.html')
def show_all_tags():
    ''' Включающий тег, отображение тегов в сайд-баре '''
    # return {'tags': TagPost.objects.all()}

    # Что бы не выводились теги, которые не прикручены к постам
    return {'tags': TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0)}

