from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from cards.models import Card
from cards.serializers import CardSerializer


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
