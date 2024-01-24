from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CirculationViewSet, ClientViewSet, MessageViewSet


router_v1 = DefaultRouter()
router_v1.register('circulations', CirculationViewSet, basename='circulations')
router_v1.register('clients', ClientViewSet, basename='clients')
router_v1.register('messages', MessageViewSet, basename='messages')


urlpatterns = [
    path('', include(router_v1.urls)),
]