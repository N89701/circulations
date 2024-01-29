from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import (
    CirculationCreateSerializer, CirculationSerializer, ClientCreateSerializer,
    ClientSerializer, MessageSerializer
)
from tables.models import Circulation, Client, Message


class CirculationViewSet(ModelViewSet):
    queryset = Circulation.objects.all().prefetch_related('filters')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CirculationSerializer
        return CirculationCreateSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all().prefetch_related('tags')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ClientSerializer
        return ClientCreateSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all().select_related('circulation', 'client')
    serializer_class = MessageSerializer
