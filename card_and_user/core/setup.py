from django.contrib.auth.models import User
from model_bakery import baker


def setupModels():
    users = list(User.objects.all())
    for i in range(len(users)):
        baker.make('cards.Card', _quantity=4, title=f'card{i}', content=f'content{i}', owner=users[i])
