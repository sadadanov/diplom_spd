from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    """
    Класс для представления модели публикации (поста)
    ...
    атрибуты
    --------
    author - автор поста
    text - текст поста
    image - фотография
    created_at - время создания
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """ метод для вывода экземпляра класса пост. """
        return f'{self.author.username} - {self.text}'


class Comment(models.Model):
    """
    Класс для представления модели комментария к посту
    ...
    атрибуты
    -------
    post - пост
    author - автор комментария
    text - текст комментария
    created_at - время создания
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """ метод для вывода экземпляра класса комментарий. """
        return f'{self.author.username} - {self.text}'


class Like(models.Model):
    """
    Класс для представления модели лайка к посту
    ...
    атрибуты
    -------
    post - пост
    author - автор лайка
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """ метод для вывода экземпляра класса лайк. """
        return f'{self.author.username} liked {self.post}'