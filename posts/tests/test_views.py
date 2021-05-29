#deals/tests/test_views.py
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post, Group

User = get_user_model()


class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='test_user')
        cls.post = Post.objects.create(
                        text='Тестовый текст',
                        author=PostsPagesTests.user,
                        group=PostsPagesTests.group
        )

        cls.post2 = Post.objects.create(
                        text='Тестовый текст',
                        author=PostsPagesTests.user,
                        group=PostsPagesTests.group
        )

        cls.group = Group.objects.create(
                        title='тестовая группа',
                        description='Описание',
                        slug='test-slug',
        )


    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostsPagesTests.user)
        self.form_fields_new_post = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            'index.html': reverse('index'),
            'new.html': reverse('new_post'),
            'group.html': reverse('group_posts',
                                  kwargs={'slug': 'test-slug'}),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Проверка словаря контекста главной страницы
    def test_home_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('index'))
        self.assertEqual(response.context.get('page').object_list[-1],
                         PostsPagesTests.post)

    # Проверка словаря context страницы group
    # и созданный пост в этой группе
    def test_group_page_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse(
            'group_posts', kwargs={'slug': 'test-slug'}
        ))
        self.assertEqual(response.context['group'], PostsPagesTests.group)
        self.assertEqual(response.context.get('page').object_list[-1],
                         PostsPagesTests.post)

    # Проверка словаря context и страницы создания поста
    def test_new_page_shows_context(self):
        """Шаблон new_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('new_post'))
        for value, expected in self.form_fields_new_post.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    # Проверка на отсутствие на страницы group другой группы созданного поста
    def test_group_pages_not_show_new_post(self):
        """Шаблон group не содержит искомый контекст."""
        response = self.authorized_client.get(
            reverse('group', kwargs={'slug': 'story'}))
        self.assertTrue(self.new_post not in response.context['posts'])

    # Проверка словаря context главной страницы index
    # и проверка на то, что созданный пост появился на главной странице
    def test_index_pages_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('index'))
        self.assertEqual(response.context['page'][0].text, 'Тестовый текст')
        self.assertEqual(response.context['page'][0].author, self.user)
        self.assertEqual(response.context['page'][0].group, self.group_story)

    # Проверка paginator: количество постов на первой странице равно 10
    def test_the_first_page_contains_ten_post_on_index_page(self):
        """Paginator работает корректно на первой странице."""
        for view in self.pages_with_posts:
            with self.subTest(view=view):
                response = self.authorized_client.get(view)
                self.assertEqual(
                    len(response.context.get('page').object_list), 10
                )

    # Проверка paginator: количество постов на второй странице равно 3
    def test_the_second_page_contains_three_post_on_index_page(self):
        """Paginator работает корректно на второй странице."""
        for view in self.pages_with_posts:
            with self.subTest(view=view):
                response = self.authorized_client.get(view + '?page=2')
                self.assertEqual(
                    len(response.context.get('page').object_list), 3
                )
