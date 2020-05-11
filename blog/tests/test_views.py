from django.test import TestCase
from django.urls import reverse

#from users.models import User
from blog.models import Article, UserUpload

class ArticleViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Article.objects.create(title='Article 3',
            date = '2020-05-10 15:53:00+02',
            )
        Article.objects.create(title='Article 4',
            date = '2020-05-10 15:58:00+02')

    def test_article_archive_index_view_status_code(self):
        response = self.client.get(reverse('blog:post_index'))
        self.assertEqual(response.status_code, 200)

    def test_article_archive_index_view_template(self):
        response = self.client.get(reverse('blog:post_index'))
        self.assertTemplateUsed(response, 'blog/article_archive.html')

    def test_article_archive_index_view_context_object(self):
        all_posts = Article.objects.all()
        response = self.client.get(reverse('blog:post_index'))
        #workaround found in
        #https://stackoverflow.com/questions/17685023/how-do-i-test-django-querysets-are-equal
        self.assertQuerysetEqual(response.context['posts'], all_posts,
            transform=lambda x: x)

    def test_article_year_archive_view_status_code(self):
        response = self.client.get(reverse('blog:post_year',
            kwargs={'year': 2020}))
        self.assertEqual(response.status_code, 200)

    def test_article_year_archive_view_template(self):
        response = self.client.get(reverse('blog:post_year',
            kwargs={'year': 2020}))
        self.assertTemplateUsed(response, 'blog/article_archive_year.html')

    def test_article_year_archive_view_context_object(self):
        all_posts = Article.objects.filter(date__year=2020)
        response = self.client.get(reverse('blog:post_year',
            kwargs={'year': 2020}))
        self.assertQuerysetEqual(response.context['posts'], all_posts,
            transform=lambda x: x)

    def test_article_month_archive_view_status_code(self):
        response = self.client.get(reverse('blog:post_month',
            kwargs={'year': 2020, 'month': 5}))
        self.assertEqual(response.status_code, 200)

    def test_article_month_archive_view_template(self):
        response = self.client.get(reverse('blog:post_month',
            kwargs={'year': 2020, 'month': 5}))
        self.assertTemplateUsed(response, 'blog/article_archive_month.html')

    def test_article_month_archive_view_context_object(self):
        all_posts = Article.objects.filter(date__year=2020, date__month=5)
        response = self.client.get(reverse('blog:post_month',
            kwargs={'year': 2020, 'month': 5}))
        self.assertQuerysetEqual(response.context['posts'], all_posts,
            transform=lambda x: x)

    def test_article_day_archive_view_status_code(self):
        response = self.client.get(reverse('blog:post_day',
            kwargs={'year': 2020, 'month': 5, 'day': 10}))
        self.assertEqual(response.status_code, 200)

    def test_article_day_archive_view_template(self):
        response = self.client.get(reverse('blog:post_day',
            kwargs={'year': 2020, 'month': 5, 'day': 10}))
        self.assertTemplateUsed(response, 'blog/article_archive_day.html')

    def test_article_day_archive_view_context_object(self):
        all_posts = Article.objects.filter(date__year=2020, date__month=5,
            date__day=10)
        response = self.client.get(reverse('blog:post_day',
            kwargs={'year': 2020, 'month': 5, 'day': 10}))
        self.assertQuerysetEqual(response.context['posts'], all_posts,
            transform=lambda x: x)

    def test_article_detail_view_status_code(self):
        response = self.client.get(reverse('blog:post_detail',
            kwargs={'year': 2020, 'month': 5, 'day': 10, 'slug': 'article-3'}))
        self.assertEqual(response.status_code, 200)

    def test_article_detail_view_template(self):
        response = self.client.get(reverse('blog:post_detail',
            kwargs={'year': 2020, 'month': 5, 'day': 10, 'slug': 'article-3'}))
        self.assertTemplateUsed(response, 'blog/article_detail.html')

    def test_article_detail_view_context_object(self):
        article = Article.objects.get(slug='article-3')
        response = self.client.get(reverse('blog:post_detail',
            kwargs={'year': 2020, 'month': 5, 'day': 10, 'slug': 'article-3'}))
        self.assertEqual(response.context['post'], article )

    #TODO test tags, test UserUpload
