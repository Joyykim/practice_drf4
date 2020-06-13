from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from cards.views import CardViewSet
from users.views import UserViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
router.register(r'cards', CardViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(r'login', views.obtain_auth_token),
]
