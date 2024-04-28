from django import template
register = template.Library()

@register.inclusion_tag('women/list_my_tag.html')
def show_my_tag():
    info = {
        'Шаг 1': 'Создаю my_tags.py. Формирую в нем информацию, указываю html-страницу (list_my_tag.html), где буду выводить ее.',
        'Шаг 2': 'Создаю html-страницу (list_my_tag.html), в ней вывожу и разукрашиваю инфу',
        'Шаг 3': 'base.html: {% load my_tags %}, вызываю фу-ю show_my_tag (Создаю my_tags.py)',
    }

    return {'info': info, }