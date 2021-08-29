from django.test import TestCase, Client

from django.conf import settings
from django.utils.translation import activate
from django.contrib.auth import get_user_model

from .. import forms


class RegistrationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        activate('en-us')
        cls.users = get_user_model()
        cls.form = forms.RegistrationForm
        cls.client = Client()
        cls.validators = [validator['NAME'] for validator in settings.AUTH_PASSWORD_VALIDATORS]

        cls.data = {
            'email': 'pinkpig@gmail.ru',
            'password1': 'e2bxBnya777',
            'password2': 'e2bxBnya777',
        }

        cls.errors = {
            'email': {
                'format': 'Enter a valid email address.',
                'overflow': 'Ensure this value has at most {} characters (it has {}).'.format(254, 310),
                'empty': 'This field is required.',
                'exists': 'The email is already in use.',
            },
            'password': {
                'empty': 'This field is required.',
                'length': 'This password is too short. It must contain at least {} characters.'.format(8),
                'pwned': 'This password is too common.',
                'numeric': 'This password is entirely numeric.',
                'similarity': 'The password is too similar to the {}.'.format('email address'),
                'mismatch': 'Password mismatch',
            }
        }

    def setUp(self):
        pass

    def test_email_bad_format(self):
        self.data['email'] = 'simple@text'
        self.assertIn(self.errors['email']['format'], self.form(self.data).errors['email'])
        self.data['email'] = '@gmail.com'
        self.assertIn(self.errors['email']['format'], self.form(self.data).errors['email'])

    def test_email_overflow(self):
        self.data['email'] = ''.join(['abc' for x in range(100)]) + '@gmail.com'
        self.assertIn(self.errors['email']['overflow'], self.form(self.data).errors['email'])

    def test_email_empty(self):
        self.data['email'] = ''
        self.assertIn(self.errors['email']['empty'], self.form(self.data).errors['email'])

    def test_email_exists(self):
        self.users.objects.create_user(email=self.data['email'])
        self.assertIn(self.errors['email']['exists'], self.form(self.data).errors['email'])

    def test_email_valid(self):
        self.assertNotIn('email', self.form(self.data).errors)

    def test_password_empty(self):
        self.data['password1'] = self.data['password2'] = ''
        self.assertIn(self.errors['password']['empty'], self.form(self.data).errors['password1'])
        self.assertIn(self.errors['password']['empty'], self.form(self.data).errors['password2'])

    def test_password_mismatch(self):
        self.data['password1'] = '1' + 'dsitkpfzwyfrhskmwj'
        self.data['password2'] = '2' + 'dsitkpfzwyfrhskmwj'
        self.assertIn(self.errors['password']['mismatch'], self.form(self.data).errors['password2'])

    # Тесты test_password_validation_* скорее всего не имеют смысла, т.к. возможны разные установки
    # в settings.AUTH_PASSWORD_VALIDATORS, а также эта функция скорее всего протестирована разработчиками
    # Django Framework. Но почему бы и нет ? :)

    def test_password_validation_numeric(self):
        if 'django.contrib.auth.password_validation.NumericPasswordValidator' in self.validators:
            self.data['password1'] = self.data['password2'] = '123456789'
            self.assertIn(self.errors['password']['numeric'], self.form(self.data).errors['password1'])

    def test_password_validation_pwned(self):
        if 'django.contrib.auth.password_validation.CommonPasswordValidator' in self.validators:
            self.data['password1'] = self.data['password2'] = '1q2w3e4r5t'
            self.assertIn(self.errors['password']['pwned'], self.form(self.data).errors['password1'])

    def test_password_validation_length(self):
        if 'django.contrib.auth.password_validation.MinimumLengthValidator' in self.validators:
            self.data['password1'] = self.data['password2'] = 'KdmaIm1'
            self.assertIn(self.errors['password']['length'], self.form(self.data).errors['password1'])

    def test_password_validation_similarity(self):
        if 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' in self.validators:
            self.data['email'] = 'jane@yandex.ru'
            self.data['password1'] = self.data['password2'] = 'yandex.ru'
            self.assertIn(self.errors['password']['similarity'], self.form(self.data).errors['password1'])

    def test_check_valid_registration(self):
        response = self.client.post('/registration/', self.data)
        existence = self.users.objects.filter(email=self.data['email']).exists()
        self.assertEqual(existence, True)


class LoginFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        activate('en-us')
        cls.users = get_user_model()
        cls.form = forms.LoginForm
        cls.client = Client()

        cls.data = {
            'enable': {'email': 'enable@ieee.org', 'password': 'e2bxBnya123'},
            'disable': {'email': 'disable@ieee.org', 'password': 'e2bxBnya123'},
            'invalid_email': {'email': 'nobody@ieee.org', 'password': 'e2bxBnya000'},
            'invalid_password': {'email': 'enable@ieee.org', 'password': '12345'}
        }

        cls.errors = {
            'incorrect': 'Incorrect email or password.'
        }

    def setUp(self):
        self.users.objects.create_user(**self.data['enable'])
        self.users.objects.create_user(**self.data['disable'], is_active=False)

    def test_inactive_user(self):
        self.assertEqual(self.form(self.data['disable']).is_valid(), False)

    def test_invalid_email(self):
        self.assertEqual(self.form(self.data['invalid_email']).is_valid(), False)

    def test_invalid_password(self):
        self.assertEqual(self.form(self.data['invalid_password']).is_valid(), False)

    def test_success_user(self):
        response = self.client.get('/login/')
        self.assertNotIn('sessionid', response.cookies.keys())

        response = self.client.post('/login/', self.data['enable'])
        self.assertIn('sessionid', response.cookies.keys())

