from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class User(TestCase):
    def test_create_user(self):
        self.usermodel = get_user_model()

        self.usermodel.objects.create_user('user1@hostname.local', '#megapassword1')
        self.usermodel.objects.create_user('user2@hostname.local', '#megapassword2', is_superuser=True)

        query1 = self.usermodel.objects.filter(email='user1@hostname.local')
        self.assertEqual(query1.count(), 1, 'user1@hostname.local don`t create')

        query2 = self.usermodel.objects.filter(email='user2@hostname.local')
        self.assertEqual(query2.count(), 1, 'user2@hostname.local don`t create')

        query1 = self.usermodel.objects.get(email='user1@hostname.local')
        self.assertEqual(query1.is_active, True)
        self.assertEqual(query1.is_superuser, False)
        self.assertEqual(query1.check_password('#megapassword1'), True)
        self.assertEqual(query1.check_password('this-is-pass'), False)

        query2 = self.usermodel.objects.get(email='user2@hostname.local')
        self.assertEqual(query2.is_superuser, True)


class Registration(TestCase):
    def test_registration(self):
        client = Client()
        self.usermodel = get_user_model()
        self.usermodel.objects.create_user('user1@hostname.local', '#megapassword1')

        response = client.get('/registration/')
        self.assertEqual(response.status_code, 200)

        response = client.post('/registration/', {
            'email': 'mail@google', 'password1': 'asd9!jaImaz', 'password2': 'asd9!jaImaz'
        })
        html = response.content.decode('UTF-8')
        self.assertIn('Введите правильный адрес электронной почты.', html)

        response = client.post('/registration/', {
            'email': 'user1@hostname.local', 'password1': '123', 'password2': '12'
        })
        html = response.content.decode('UTF-8')
        self.assertIn('The email is already in use', html)
        self.assertIn('Password mismatch', html)
        self.assertIn('Введённый пароль слишком широко распространён.', html)
        self.assertIn('Введённый пароль состоит только из цифр.', html)
        self.assertIn('Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов.', html)

        response = client.post('/registration/', {
            'email': 'maxemilian@m.ru', 'password1': 'maxemilian', 'password2': 'maxemilian'
        })
        html = response.content.decode('UTF-8')
        self.assertIn('Введённый пароль слишком похож на адрес электронной почты.', html)

        response = client.post('/registration/', {
            'email': 'maxemilian@m.ru', 'password1': 'ihs&dalac!932', 'password2': 'ihs&dalac!932'
        })
        query = self.usermodel.objects.filter(email='maxemilian@m.ru').exists()
        self.assertEqual(query, True)