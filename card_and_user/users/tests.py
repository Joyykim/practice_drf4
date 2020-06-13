from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from munch import Munch
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from model_bakery import baker


class UserTestCase(APITestCase):

    # 모든 테스트 메소드의 실행 전에 실행됨!
    def setUp(self) -> None:
        self.users = baker.make('auth.User', _quantity=3)

    def test_should_list(self):
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get('/api/users')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 모든 유저 돌려서 확인
        for user_response, user in zip(response.data['results'], self.users[::-1]):
            self.assertEqual(user_response['id'], user.id)
            self.assertEqual(user_response['username'], user.username)

        # 테스트 강제 fail
        # self.fail()

    def test_should_create(self):
        data = {'username': 'new_one'}
        response = self.client.post('/api/users', data=data)
        self.client.force_authenticate(user=self.users[1])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_response = Munch(response.data)
        self.assertTrue(user_response.id)
        self.assertEqual(user_response.username, data['username'])

    def test_should_get(self):
        user = self.users[0]
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/users/{user.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_response = Munch(response.data)
        self.assertTrue(user_response.id)
        self.assertEqual(user_response.username, user.username)

    def test_should_update(self):
        user = self.users[0]
        prev_username = user.username

        data = {"username": "new"}
        self.client.force_authenticate(user=self.users[1])
        response = self.client.put(f'/api/users/{user.id}', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_response = Munch(response.data)
        self.assertTrue(user_response.id)
        self.assertEqual(user_response.username, data['username'])
        self.assertNotEqual(user_response.username, prev_username)

    def test_should_delete(self):
        user = self.users[0]

        self.client.force_authenticate(user=user)
        response = self.client.delete(f'/api/users/{1}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(User.objects.filter(pk=user.id).exists())

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=user.id)

    # 커스텀 메소드 테스트
    def test_logout(self):
        user = self.users[1]
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/users/logout')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user_id=user.id).exists())
