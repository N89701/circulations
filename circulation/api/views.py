from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import (
    CirculationCreateSerializer, CirculationSerializer, ClientCreateSerializer,
    ClientSerializer, MessageSerializer
)
from tables.models import Circulation, Client, Message


class CirculationViewSet(ModelViewSet):
    queryset = Circulation.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CirculationSerializer
        return CirculationCreateSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ClientSerializer
        return ClientCreateSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
