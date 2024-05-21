menu = [
    {'title': 'О сайтище', 'url_name': 'about'},
    {'title': 'Что-то добавить', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Стать своим', 'url_name': 'login'},
]


class DataMixin:
    '''
    Это Миксин
    помогает сократить дублирование кода в тексте программы
    '''
    # Пагинация. Когда используется ListView, то автоматически в шаблон
    # передаются переменные paginator & page_obj
    paginate_by = 5
    title_page = None
    cat_selected = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.cat_selected is not None:
            # Явно проверяю, что не None (0-->False)
            self.extra_context['cat_selected'] = self.cat_selected

        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

    def get_mixin_context(self, context, **kwargs):
        ''' Расширю context '''
        context['menu'] = menu
        context['cat_selected'] = None
        context.update(kwargs)
        return context
