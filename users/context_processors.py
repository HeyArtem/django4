from women.utils import menu


def get_women_context(request):
    '''
        Шаблонный контекстный процессор.
        Я пропишу его в settings.
        Использовать это нужно для данных, которые передаются во все шаблоны,
        'mainmenu' - будет доступна во всех шаблонах
    '''
    return {'mainmenu': menu}
