from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from .serializers import ReadOnlyUserSerializer, WriteOnlyUserSerializer


class FilmViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # (1)import django
        cls.user1 = User.objects.create_user('user1', password='password1')
        cls.user2 = User.objects.create_user('user2', password='password2')
        cls.admin = User.objects.create_superuser('admin', password='password')

    def test_list_users_as_admin(self):
        token = self.client.post(reverse("auth-token"), {"username": "admin", "password": "password"}).data['token']
        self.client_class.credentials(self.client, HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse("api-users-list"))
        requested_users = response.data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(ReadOnlyUserSerializer(instance=self.user1).data, requested_users[0])
        self.assertEquals(ReadOnlyUserSerializer(instance=self.user2).data, requested_users[1])

    def test_get_user_by_id(self):
        response = self.client.get(
            reverse("api-users-detail", args=[self.user1.id])
        )

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(
            ReadOnlyUserSerializer(instance=self.user1).data,
            response.data
        )

    def test_post_user(self):
        self.client.post(
            reverse("api-users-list"),
            data={'username': 'user3',
                  'password': 'pass3'}
        )

        self.assertEquals(len(User.objects.all()), 4)

    def test_patch_user(self):
        token = self.client.post(reverse("auth-token"), {"username": "user2", "password": "password2"}).data['token']
        self.client_class.credentials(self.client, HTTP_AUTHORIZATION='Token ' + token)
        self.client.patch(
            reverse("api-users-detail", args=[2]),
            data={'username': 'user22',
                  'password': 'pass33'}
        )
        new_username = User.objects.get(id=2).username
        self.assertEquals(new_username, 'user22')

    def test_delete_user(self):
        token = self.client.post(reverse("auth-token"), {"username": "admin", "password": "password"}).data['token']
        self.client_class.credentials(self.client, HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete(
            reverse("api-users-detail", args=[2])
        )
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)