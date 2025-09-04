from rest_framework import serializers
from models import Comment, Post


class CommentSerializer(serializers.ModelSerializer):
    """ Класс для представления сериализатора комментария. """
    class Meta:
        model = Comment
        fields = ['author', 'text', 'created_at']
        read_only_fields = ['author']


class PostSerializer(serializers.ModelSerializer):
    """ Класс для представления сериализатора поста. """
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'text', 'image', 'created_at', 'comments']

    def to_representation(self, post):
        """ Метод вывода количества лайков в посте """
        representation = super().to_representation(post)
        representation['likes_count'] = post.likes.count()
        return representation