from django.test import TestCase

from blog.models import Article

class ArticleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Article.objects.create(title='Article 1')

    def test_article_str_method(self):
        article = Article.objects.get(id = 1)
        self.assertEquals(article.__str__(), 'Article 1')
