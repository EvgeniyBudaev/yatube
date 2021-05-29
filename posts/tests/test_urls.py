# posts/tests/tests_url.py
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Group

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        self.guest_client = Client()

    def test_homepage(self):
        # Отправляем запрос через client,
        # созданный в setUp()
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Test title',
            slug='slug',
            description='Test description'
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованый клиент
        self.user = User.objects.create_user(username='EvgeniyBudaev')
        # Создаем второго неавторизованного клиента
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)
        # Список URL адресов
        self.url_names = ['/', '/group/slug/', '/new/']
        # Доступные URL для анонимного пользователя
        self.templates_url_names_anonymous = {
            'posts/index.html': '/',
            'posts/group.html': '/group/slug/',
        }
        # Доступные URL для авторизованного пользователя
        self.templates_url_names_authorized = {
            'posts/index.html': '/',
            'posts/group.html': '/group/slug/',
            'posts/new_post.html': '/new/',
        }

    # Проверяем доступность страниц для анонимного пользователя
    def test_url_exists_at_desired_location_for_anonymous(self):
        """URL страниц доступные анонимным
        пользователям."""
        for url in self.url_names[:2]:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    # Проверяем доступность страниц для анонимного пользователя
    def test_url_exists_at_desired_location_for_authorized(self):
        """URL страниц доступные авторизованным пользователям."""
        for url in self.url_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, 200)

    # Проверяем доступность шаблонов для авторизованного пользователя
    def test_urls_uses_correct_template_anonymous(self):
        """URL-адрес использует соответствующий шаблон для анонимного
        пользователя."""
        for template, url in self.templates_url_names_anonymous.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)

    # Проверяем доступность шаблонов для авторизованного пользователя
    def test_urls_uses_correct_template_authorized(self):
        """URL-адрес использует соответствующий шаблон
        для авторизованного пользователя."""
        for template, url in self.templates_url_names_authorized.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    # Проверяем редиректы для неавторизованного пользователя
    def test_task_detail_url_redirect_anonymous(self):
        """Страница /new/ перенаправляет анонимного
        пользователя.
        """
        response = self.guest_client.get('/new/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/new/')
