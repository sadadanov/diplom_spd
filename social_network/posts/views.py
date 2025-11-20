from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from models import Post, Comment, Like
from permissions import IsOwnerOrReadOnly
from serializers import PostSerializer, CommentSerializer


class PostViewSet(ModelViewSet):
    """
    Класс для представления вьюсета публикации (поста).
    Атрибуты
    --------
    queryset - кверисет
    serializer_class - сериализатор
    Методы
    ------
    get_permissions - метод динамического определение
                      списка разрешений для представления
    perform_create - метод создания объекта пост
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        """ Метод получения прав для действий с объектом пост. """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return [IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        """
        Метод создания поста
        для передачи аутентифицированного по токену пользователя
        """
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    """ Класс для представления вьюсета комментария. """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """
        Метод создания комментария
        для передачи идентификатора поста
        и аутентифицированного по токену пользователя
        """
        serializer.save(post_id=self.kwargs['post_id'],
                        author=self.request.user)


class LikeView(APIView):
    """
    Класс для представления вьюсета лайка.

    Атрибут permission_classes - указывает список разрешений выполняемых
                                 для доступа к представлению
    Методы
    ------
    post - создание лайка в посте
    delete - удаление лайка в посте
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        """ Метод создания лайка в посте. """
        
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"Ошибка": "Пост не найден."}, status=status.HTTP_404_NOT_FOUND)

        user = self.request.user

        if Like.objects.filter(post=post, author=user).exists():
            return Response({"Ошибка": "Вы уже оценили этот пост"}, status=status.HTTP_400_BAD_REQUEST)
               
        if not Like.objects.filter(post=post, author=request.user).exists():
            Like.objects.create(post=post, author=request.user)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        """ Метод удаления лайка в посте. """
        
         try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"Ошибка": "Пост не найден."}, status=status.HTTP_404_NOT_FOUND)
        
        if Like.objects.filter(post=post, author=request.user).exists():
            Like.objects.filter(post=post, author=request.user).delete()
        return Response(status=status.HTTP_200_OK)
