from .test_setup import TestSetUp
from rest_framework import status
from rest_framework.test import force_authenticate
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
        response = self.client.post(self.short_text_url, data=self.text_data[0])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorised_user_can_post_shorttexts(self):
        self.client.post(self.register_url, data=self.user_data)
        user = User.objects.get(username=self.user_data['username'])
        view = ShortTextViewSet.as_view({'post': 'create'})

        post_request = self.factory.post(self.short_text_url, data=self.text_data[0])
        force_authenticate(post_request, user=user)
        response = view(post_request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], self.text_data[0]['text'])

    def test_authorised_user_can_update(self):
        self.client.post(self.register_url, data=self.user_data)
        user = User.objects.get(username=self.user_data['username'])
        view = ShortTextViewSet.as_view({'post': 'create', 'put': 'update'})

        post_request = self.factory.post(self.short_text_url, data=self.text_data[0])
        force_authenticate(post_request, user=user)
        pk = str(view(post_request).data['text_id'])
        url = f'{self.short_text_url}{pk}/'

        put_request = self.factory.put(url, data=self.text_data[1])
        force_authenticate(put_request, user=user)
        response = view(put_request, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], self.text_data[1]['text'])

    def test_unauthorised_user_cant_update(self):
        self.client.post(self.register_url, data=self.user_data)
        user = User.objects.get(username=self.user_data['username'])
        view = ShortTextViewSet.as_view({'post': 'create', 'put': 'update'})

        post_request = self.factory.post(self.short_text_url, data=self.text_data[0])
        force_authenticate(post_request, user=user)
        pk = str(view(post_request).data['text_id'])
        url = f'{self.short_text_url}{pk}/'

        put_request = self.factory.put(url, data=self.text_data[1])
        response = view(put_request, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorised_user_can_delete(self):
        self.client.post(self.register_url, data=self.user_data)
        user = User.objects.get(username=self.user_data['username'])
        view = ShortTextViewSet.as_view({'post': 'create', 'delete': 'destroy'})

        post_request = self.factory.post(self.short_text_url, data=self.text_data[0])
        force_authenticate(post_request, user=user)
        pk = str(view(post_request).data['text_id'])
        url = f'{self.short_text_url}{pk}/'

        delete_request = self.factory.delete(url)
        force_authenticate(delete_request, user=user)
        response = view(delete_request, pk=pk)
        self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK, status.HTTP_202_ACCEPTED])

    def test_unauthorised_user_cant_delete(self):
        self.client.post(self.register_url, data=self.user_data)
        user = User.objects.get(username=self.user_data['username'])
        view = ShortTextViewSet.as_view({'post': 'create', 'delete': 'destroy'})

        post_request = self.factory.post(self.short_text_url, data=self.text_data[0])
        force_authenticate(post_request, user=user)
        pk = str(view(post_request).data['text_id'])
        url = f'{self.short_text_url}{pk}/'

        delete_request = self.factory.delete(url)
        response = view(delete_request, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_viewcount_works(self):
        self.client.post(self.register_url, data=self.user_data)
        user = User.objects.get(username=self.user_data['username'])
        view = ShortTextViewSet.as_view({'post': 'create', 'put': 'update'})

        # Testing viewcount upon creation
        post_request = self.factory.post(self.short_text_url, data=self.text_data[0])
        force_authenticate(post_request, user=user)
        response = view(post_request)
        self.assertEqual(response.data['viewcount'], 0)

        # Testing viewwcount in list view
        response = self.client.get(self.short_text_url)
        self.assertEqual(response.data[0]['viewcount'], 1)
        pk = str(response.data[0]['text_id'])
        url = f'{self.short_text_url}{pk}/'

        # Testing viewcount in instance view
        response = self.client.get(url)
        self.assertEqual(response.data['viewcount'], 2)

        # Testing instance view multiple times
        for i in range(1, 11):
            response = self.client.get(url)
            self.assertEqual(response.data['viewcount'], 2 + i)

        # Testing if updating resets viewcount
        put_request = self.factory.put(url, data=self.text_data[1])
        force_authenticate(put_request, user=user)
        response = view(put_request, pk=pk)
        self.assertEqual(response.data['viewcount'], 0)

    def test_blank_texts_are_not_accepted(self):
        self.client.post(self.register_url, data=self.user_data)
        user = User.objects.get(username=self.user_data['username'])
        view = ShortTextViewSet.as_view({'post': 'create'})

        # Posting a blank text
        post_request = self.factory.post(self.short_text_url, data={'text': ''})
        force_authenticate(post_request, user=user)
        response = view(post_request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_max_text_length_is_160_chars(self):
        self.client.post(self.register_url, data=self.user_data)
        user = User.objects.get(username=self.user_data['username'])
        view = ShortTextViewSet.as_view({'post': 'create'})

        # Posting a 160 chars long text
        post_request = self.factory.post(self.short_text_url, data={'text': 'a' * 160})
        force_authenticate(post_request, user=user)
        response = view(post_request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], 'a' * 160)

        # Posting a 161 chars long text
        post_request = self.factory.post(self.short_text_url, data={'text': 'a' * 161})
        force_authenticate(post_request, user=user)
        response = view(post_request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
