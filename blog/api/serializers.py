from rest_framework import serializers

from blog.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False, read_only=False)
    class Meta:
        model = Article
        fields = [ 'uuid', 'title', 'slug', 'intro', 'date', 'last_updated',
            'body', 'author', ]
