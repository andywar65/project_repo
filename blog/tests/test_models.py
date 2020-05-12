from django.test import TestCase

from users.models import User
from streamblocks.models import IndexedParagraph, LandscapeGallery
from blog.models import Article, UserUpload

class ArticleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        IndexedParagraph.objects.create(id=47, title='Foo', body='Bar')
        LandscapeGallery.objects.create(id=48, fb_image='uploads/image.jpg')
        Article.objects.create(title='Article 1',
            date = '2020-05-09 15:53:00+02',
            stream = '[{"unique_id":"4h5dps","model_name":"IndexedParagraph","id":47,"options":{}}]',
            carousel = '[{"unique_id":"dps4h5","model_name":"LandscapeGallery","id":[48],"options":{}}]',
            notice = 'SPAM'
            )
        Article.objects.create(title='Article 2',
            date = '2020-05-09 15:58:00+02')
        User.objects.create(username='andywar65', password='P4s5W0r6')
        article = Article.objects.get(slug='article-1')
        user = User.objects.get(username='andywar65')
        UserUpload.objects.create(id=49, post=article, user=user,
            body='Foo Bar')

    def test_article_get_image(self):
        article = Article.objects.get(slug='article-1')
        #here I extract the FilObject.path for convenience
        self.assertEquals(article.get_image().path, 'uploads/image.jpg')

    def test_article_str_method(self):
        article = Article.objects.get(slug='article-1')
        self.assertEquals(article.__str__(), 'Article 1')

    def test_article_get_path(self):
        article = Article.objects.get(slug='article-1')
        self.assertEquals(article.get_path(), '/articoli/2020/05/09/article-1')

    def test_article_get_previous(self):
        article = Article.objects.get(slug='article-1')
        self.assertEquals(article.get_previous(), None)

    def test_article_get_next(self):
        article = Article.objects.get(slug='article-1')
        article_2 = Article.objects.get(slug='article-2')
        self.assertEquals(article.get_next(), article_2)

    def test_article_get_uploads(self):
        article = Article.objects.get(slug='article-1')
        uploads = UserUpload.objects.filter(post_id=article.id)
        #workaround found in
        #https://stackoverflow.com/questions/17685023/how-do-i-test-django-querysets-are-equal
        self.assertQuerysetEqual(article.get_uploads(), uploads,
            transform=lambda x: x)

    def test_article_notice_status(self):
        article = Article.objects.get(slug='article-1')
        self.assertEquals(article.notice, 'DONE')

    def test_article_stream_search(self):
        article = Article.objects.get(slug='article-1')
        self.assertEquals(article.stream_search,
            '\n  \n    Foo\n    \n  \n  \n     Bar \n  \n\n')

    def test_userupload_str_method(self):
        upload = UserUpload.objects.get(id = 49)
        self.assertEquals(upload.__str__(), 'Contributo - 49')
