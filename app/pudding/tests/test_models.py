from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model


class UserManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.model = get_user_model()

    def setUp(self):
        self.user = self.model.objects.create_user(
            email='user@test.ru',
            password='p@ssword777')

        self.superuser = self.model.objects.create_user(
            email='superuser@test.ru',
            password='p@ssword777',
            is_superuser=True)

    def test_check_settings(self):
        um = getattr(settings, 'AUTH_USER_MODEL', None)
        self.assertNotEqual(um, None)
        self.assertEqual(um, 'pudding.User')

    def test_user_exists(self):
        existence = self.model.objects.filter(email='user@test.ru').exists()
        self.assertEqual(existence, True)

    def test_superuser_exists(self):
        existence = self.model.objects.filter(email='superuser@test.ru').exists()
        self.assertEqual(existence, True)

    def test_check_flag_is_superuser(self):
        user = self.model.objects.get(email='user@test.ru')
        superuser = self.model.objects.get(email='superuser@test.ru')
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(superuser.is_superuser, True)

    def test_check_password(self):
        user = self.model.objects.get(email='user@test.ru')
        password = user.check_password('p@ssword777')
        self.assertEqual(password, True)
