from .test_setup import TestSetUp
from rest_framework import status
from rest_framework.test import force_authenticate, APIRequestFactory
from django.contrib.auth.models import User
from ..views import ShortTextViewSet


class TestViews(TestSetUp):

    def test_user_cannot_register_with_no_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register(self):
        response = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertEqual(response.data['email'], self.user_data['email'])
        self.assertEqual(response.data['first_name'], self.user_data['first_name'])
        self.assertEqual(response.data['last_name'], self.user_data['last_name'])

    def test_registered_user_can_login(self):
        self.client.post(self.register_url, data=self.user_data)
        response = self.client.post(self.login_url, data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_unauthorised_user_can_view_shorttexts(self):
        response = self.client.get(self.short_text_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorised_user_cant_post_shorttexts(self):
        response = self.client.post(self.short_text_url, data={'text': 'hello'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorised_user_can_post_shorttexts(self):
        self.client.post(self.register_url, data=self.user_data)
        user = User.objects.get(username=self.user_data['username'])
        view = ShortTextViewSet.as_view({'post': 'create'})
        request = self.factory.post(self.short_text_url, data={'text': 'hello'})
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], 'hello')
