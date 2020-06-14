from rest_framework.fields import ReadOnlyField, Field

from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from cards.models import Card


class CardSerializer(ModelSerializer):
    owner = ReadOnlyField(source='owner.id')

    class Meta:
        model = Card
        fields = ('id', 'title', 'content', 'like', 'is_reported', 'owner')
