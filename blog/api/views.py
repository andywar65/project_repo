from rest_framework.generics import ( ListCreateAPIView,
    RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from blog.models import Article
from .serializers import ArticleSerializer

class ArticleListCreateAPIView(ListCreateAPIView):
    queryset = Article.objects.all()
    #permission_classes = (IsAuthenticated, )
    serializer_class = ArticleSerializer
    lookup_field = 'uuid'

class ArticleRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    #permission_classes = (IsAuthenticated, )
    serializer_class = ArticleSerializer
    lookup_field = 'uuid'
