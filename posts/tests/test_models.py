from django.test import TestCase
from django.contrib.auth import get_user_model

from posts.models import Group, Post

User = get_user_model()


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.group = Group.objects.create(
            title='Тестовый текст'
        )

    def test_object_name_is_title_field(self):
        """В поле __str__  объекта group записано значение поля group.title."""
        group = GroupModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create(
            username='author',
        )

        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )

    def test_object_name_is_text_field(self):
        """В поле __str__  объекта post записано значение поля post.text."""
        post = PostModelTest.post
        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name, str(post))
