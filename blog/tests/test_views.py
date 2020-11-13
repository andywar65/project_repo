from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group

from taggit.models import Tag

from users.models import User
from blog.models import Article, UserUpload

class ArticleViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        tag = Tag.objects.create( name='foo' )
        usr = User.objects.create_user(username='logged_in',
            password='P4s5W0r6')
        group = Group.objects.get(name='Trusted')
        usr.groups.add(group)

        User.objects.create_user(username='untrusted',
            password='P4s5W0r6')
        article = Article.objects.create(title='Article 3',
            date = '2020-05-10', author = usr
            )
        #article.tags.add('foo')
        Article.objects.create(title='Article 4',
            date = '2020-05-10')
        UserUpload.objects.create(user=usr, post=article, body='Foo Bar')

    def test_article_archive_index_view_status_code(self):
        response = self.client.get(reverse('blog:post_index'))
        self.assertEqual(response.status_code, 200)

    def test_article_archive_index_view_template(self):
        response = self.client.get(reverse('blog:post_index'))
        self.assertTemplateUsed(response, 'blog/article_archive.html')

    def test_article_archive_index_view_template_tagged(self):
        response = self.client.get('/articoli/?tag=foo')
        self.assertTemplateUsed(response, 'blog/article_archive.html')

    def test_article_archive_index_view_context_object(self):
        all_posts = Article.objects.all()
        response = self.client.get(reverse('blog:post_index'))
        #workaround found in
        #https://stackoverflow.com/questions/17685023/how-do-i-test-django-querysets-are-equal
        self.assertQuerysetEqual(response.context['posts'], all_posts,
            transform=lambda x: x)

    def test_article_archive_index_view_context_object_tagged(self):
        all_posts = Article.objects.filter( tags__name='foo' )
        response = self.client.get('/articoli/?tag=foo')
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

    def test_author_list_view_status_code(self):
        response = self.client.get(reverse('blog:post_authors'))
        self.assertEqual(response.status_code, 200)

    def test_author_list_view_template(self):
        response = self.client.get(reverse('blog:post_authors'))
        self.assertTemplateUsed(response, 'blog/author_list.html')

    def test_author_list_view_context_object(self):
        all_users = User.objects.all()
        response = self.client.get(reverse('blog:post_authors'))
        self.assertQuerysetEqual(response.context['user_list'], all_users,
            transform=lambda x: x )

    def test_author_list_view_context_authors(self):
        usr = User.objects.get(username='logged_in')
        response = self.client.get(reverse('blog:post_authors'))
        #here we have only one author
        self.assertEqual(response.context['authors'], {usr: (1,1)} )

    def test_by_author_list_view_status_code(self):
        usr = User.objects.get(username='logged_in')
        response = self.client.get(reverse('blog:post_by_author',
            kwargs={ 'username' : usr.username }))
        self.assertEqual(response.status_code, 200)

    def test_by_author_list_view_template(self):
        usr = User.objects.get(username='logged_in')
        response = self.client.get(reverse('blog:post_by_author',
            kwargs={ 'username' : usr.username }))
        self.assertTemplateUsed(response, 'blog/article_archive_authors.html')

    def test_by_author_list_view_context_object(self):
        usr = User.objects.get(username='logged_in')
        posts = Article.objects.filter( author_id=usr.uuid )
        response = self.client.get(reverse('blog:post_by_author',
            kwargs={ 'username' : usr.username }))
        self.assertQuerysetEqual(response.context['posts'], posts,
            transform=lambda x: x )

    def test_by_author_list_view_context_object_tagged(self):
        usr = User.objects.get(username='logged_in')
        posts = Article.objects.filter( author_id=usr.uuid, tags__name='foo' )
        response = self.client.get(f'/articoli/autori/{usr.username}/?tag=foo')
        self.assertQuerysetEqual(response.context['posts'], posts,
            transform=lambda x: x )

    def test_by_upload_list_view_status_code(self):
        usr = User.objects.get(username='logged_in')
        response = self.client.get(reverse('blog:upload_by_author',
            kwargs={ 'username' : usr.username }))
        self.assertEqual(response.status_code, 200)

    def test_by_upload_list_view_template(self):
        usr = User.objects.get(username='logged_in')
        response = self.client.get(reverse('blog:upload_by_author',
            kwargs={ 'username' : usr.username }))
        self.assertTemplateUsed(response, 'blog/uploads_by_author.html')

    def test_by_upload_list_view_context_object(self):
        usr = User.objects.get(username='logged_in')
        uploads = UserUpload.objects.filter( user_id=usr.uuid )
        response = self.client.get(reverse('blog:upload_by_author',
            kwargs={ 'username' : usr.username }))
        self.assertQuerysetEqual(response.context['uploads'], uploads,
            transform=lambda x: x )

    def test_user_upload_create_view_redirect_not_logged(self):
        response = self.client.get('/articoli/contributi/?post_id=34')
        self.assertRedirects(response,
            '/account/login/?next=/articoli/contributi/%3Fpost_id%3D34')

    def test_user_upload_create_view_status_code(self):
        self.client.post('/account/login/', {'username':'logged_in',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('blog:post_upload'))
        self.assertEqual(response.status_code, 200)

    def test_user_upload_create_view_status_code_untrusted(self):
        self.client.post('/account/login/', {'username':'untrusted',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('blog:post_upload'))
        self.assertEqual(response.status_code, 403)

    def test_user_upload_create_view_status_code_untrusted_explicit(self):
        self.client.post('/account/login/', {'username':'untrusted',
            'password':'P4s5W0r6'})
        response = self.client.get('/articoli/contributi/?post_id=34')
        self.assertEqual(response.status_code, 403)

    def test_user_upload_create_view_template(self):
        self.client.post('/account/login/', {'username':'logged_in',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('blog:post_upload'))
        self.assertTemplateUsed(response, 'blog/userupload_form.html')

    def test_user_upload_create_view_success_url(self):
        self.client.post('/account/login/', {'username':'logged_in',
            'password':'P4s5W0r6'})
        article = Article.objects.get(slug='article-3')
        response = self.client.post(f'/articoli/contributi/?post_id={article.slug}',
            {'body': 'Foo Bar'})
        self.assertRedirects(response,
            '/articoli/2020/05/10/article-3/#upload-anchor')
