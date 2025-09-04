from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Класс для создания пользовательского разрешения на работу с постами и комментариями.
    """
    def has_object_permission(self, request, view, obj):
        """
        Метод для проверки прав пользователя на конкретный объект поста или комментария.
        """
        # если запрос на чтение, то разрешаем иначе проверяем совпадает ли
        # пользователь из запроса с пользователем создавшим данный объект
        if request.method == 'GET':
            return True
        return request.user == obj.author