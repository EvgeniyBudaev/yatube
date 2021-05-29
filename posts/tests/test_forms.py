from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='Evgeniy')
        cls.post = Post.objects.create(
                        text='Тестовый текст',
                        author=PostFormTests.user
                        )

    def setUp(self):
        """Создание авторизованного пользователя."""
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTests.user)

    def test_post_form_create_new_post(self):
        """Валидная форма создает запись в Posts."""
        # Подсчитаем количество записей в Post
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст нового поста для формы'
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект на главную страницу
        self.assertRedirects(response, reverse('index'))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count+1)
        # Проверяем, что создалась запись с нашим текстом
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
            ).exists()
        )
