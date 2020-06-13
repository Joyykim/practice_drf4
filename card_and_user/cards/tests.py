from cards.models import Card
from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase
from model_bakery import baker


class CardTestCase(APITestCase):

    # 모든 테스트 메소드의 실행 전에 실행됨!
    def setUp(self) -> None:
        self.users = baker.make('auth.User', _quantity=3)
        self.cards = baker.make('cards.Card', _quantity=4, content='dsds', owner=self.users[0])
        self.cards += baker.make('cards.Card', _quantity=4, content='dsds', owner=self.users[1])
        self.cards += baker.make('cards.Card', _quantity=4, content='dsds', owner=self.users[2])

        self.user = self.users[1]
        self.card = Card.objects.filter(owner_id=self.user.id).first()

    def test_should_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/cards')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 모든 유저 돌려서 확인
        for card_response, card in zip(response.data['results'], self.cards[::-1]):
            self.assertEqual(card_response['content'], card.content)
            self.assertEqual(card_response['id'], card.id)

    def test_should_create(self):
        data = {"content": "blah blah blah", "owner_id": self.user.id}
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/cards', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        card_response = Munch(response.data)
        self.assertTrue(card_response.id)
        self.assertEqual(card_response.content, data['content'])
        self.assertEqual(card_response.owner, self.user.username)

    def test_should_retrieve(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/cards/{self.card.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        card_response = Munch(response.data)
        self.assertTrue(card_response.id)
        self.assertEqual(card_response.content, self.card.content)

    def test_should_update(self):
        prev_content = self.card.content
        data = {"content": "new new blah blah blah"}

        self.client.force_authenticate(user=self.user)
        response = self.client.put(f'/api/cards/{self.card.id}', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_response = Munch(response.data)
        self.assertTrue(user_response.id)
        self.assertEqual(user_response.content, data['content'])
        self.assertNotEqual(user_response.content, prev_content)

    def test_should_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/cards/{self.card.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Card.objects.filter(pk=self.card.id).count(), 0)

        # with self.assertRaises(Card.DoesNotExist):
        #     User.objects.get(pk=self.card.id)

        # self.fail()

    # 커스텀 메소드 테스트
    # def test(self):
    #     self.client.force_authenticate(user=self.users[0])
    #     self.client.get('/api/users/fast')
