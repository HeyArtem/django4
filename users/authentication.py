from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        '''
            Аутентификация пользователя по e-mail
            user_model-получаю текущую модель пользователя,
            пробую получить пользователя по модели (username буду использовать, как маил),
            если успешно, то проверяю совпадение пароля (check_password)
                возвращаю объект user | None
            Прописываю исключения:
                DoesNotExist-не нашел запись
                MultipleObjectsReturned-нашел несколько записей по email
        '''
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        '''
            Возвращает объект user (отображение имени, под кем зашел
            пользователь, ИМЯ | Регистрация)
        '''
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
