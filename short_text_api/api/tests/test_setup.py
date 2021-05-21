from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse
from faker import Faker


class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = '/api-auth/login/'
        self.short_text_url = '/shorttexts/'
        self.factory = APIRequestFactory()
        self.faker = Faker()

        user = self.faker.profile(['name', 'mail', 'username'])
        self.text_data = [{'text': self.faker.paragraph(nb_sentences=1)} for i in range(3)]
        self.user_data = {
            'email': user['mail'],
            'username': user['username'],
            'password': '_'.join(user['name'].lower().split()),
            'password2': '_'.join(user['name'].lower().split()),
            'first_name': user['name'].split()[0],
            'last_name': user['name'].split()[1],
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
