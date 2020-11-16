from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from users.models import User, Profile
from pages.models import GalleryImage
from blog.models import Article, UserUpload

class ArticleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='andywar65', password='P4s5W0r6',
            email='andy@war.com')
        profile = Profile.objects.get(pk=user.uuid)
        profile.yes_spam = True
        profile.save()
        recipient = User.objects.create(username='recipient', password='P4s5W0r6',
            email='recipient@war.com')
        profile = Profile.objects.get(pk=recipient.uuid)
        profile.yes_spam = True
        profile.save()
        article = Article.objects.create(title='Article 1',
            date = '2020-05-09',
            body = 'Foo Bar',
            notice = 'SPAM'
            )
        #GalleryImage.objects.create(post_id=article.uuid, fb_image='uploads/image.jpg')
        #GalleryImage.objects.create(post_id=article.uuid, fb_image='uploads/image2.jpg')
        Article.objects.create(title='Article 2',
            date = '2020-05-10')
        UserUpload.objects.create(id=49, post=article, user=user,
            body='Foo Bar')

    #def test_article_get_image(self):
        #article = Article.objects.get(slug='article-1')
        #here I extract the FilObject.path for convenience
        #self.assertEquals(article.get_image().path, 'uploads/image.jpg')

    def test_article_str_method(self):
        article = Article.objects.get(slug='article-1')
        self.assertEquals(article.__str__(), 'Article 1')

    def test_article_get_path(self):
        article = Article.objects.get(slug='article-1')
        self.assertEquals(article.get_path(),
            reverse('blog:post_index')+'2020/05/09/article-1')

    def test_article_get_previous(self):
        article = Article.objects.get(slug='article-1')
        self.assertEquals(article.get_previous(), None)

    def test_article_get_next(self):
        article = Article.objects.get(slug='article-1')
        article_2 = Article.objects.get(slug='article-2')
        self.assertEquals(article.get_next(), article_2)

    def test_article_get_next_missing(self):
        article_2 = Article.objects.get(slug='article-2')
        self.assertEquals(article_2.get_next(), None)

    def test_article_get_uploads(self):
        article = Article.objects.get(slug='article-1')
        uploads = UserUpload.objects.filter(post_id=article.uuid)
        #workaround found in
        #https://stackoverflow.com/questions/17685023/how-do-i-test-django-querysets-are-equal
        self.assertQuerysetEqual(article.get_uploads(), uploads,
            transform=lambda x: x)

    def test_article_notice_status(self):
        article = Article.objects.get(slug='article-1')
        self.assertEquals(article.notice, 'DONE')

    def test_userupload_str_method(self):
        upload = UserUpload.objects.get(id = 49)
        self.assertEquals(upload.__str__(), _('Contribution')+' - 49')
