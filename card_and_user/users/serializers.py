from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from cards.serializers import CardSerializer


class UserSerializer(ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'cards')
