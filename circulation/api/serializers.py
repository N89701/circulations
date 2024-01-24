from django.db import transaction
from django.db.models import F
from rest_framework.serializers import (
    DateTimeField, ImageField, IntegerField, ModelSerializer,
    PrimaryKeyRelatedField, SerializerMethodField, ValidationError
)

from tables.models import (
    Circulation, CirculationFilter, Client, Filter, Message, Tag
)


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'

class CirculationFilterCreateSerializer(ModelSerializer):

    class Meta:
        model = CirculationFilter
        fields = ('filter', 'value')


class CirculationCreateSerializer(ModelSerializer):
    filters = CirculationFilterCreateSerializer(many=True)

    class Meta:
        model = Circulation
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        filters = validated_data.pop('filters')
        circulation = Circulation.objects.create(**validated_data)
        # circulation.filters.set(filters)
        self.circulationfilter_create(filters, circulation)
        return circulation

    @staticmethod
    def circulationfilter_create(objs, circulation):
        CirculationFilter.objects.bulk_create(
            CirculationFilter(
                circulation=circulation,
                filter=obj['filter'],
                value=obj['value'])
            for obj in objs
        )
    
    def to_representation(self, instance):
        return CirculationSerializer(instance, context=self.context).data


class CirculationSerializer(ModelSerializer):
    filters = SerializerMethodField()

    class Meta:
        model = Circulation
        fields = '__all__'

    def get_filters(self, circulation):
        return circulation.filters.values(
            'id',
            'circulation',
            value=F('circulationfilter__value')
        )


class ClientCreateSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'


class ClientSerializer(ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Client
        fields = '__all__'


class MessageSerializer(ModelSerializer):
    circulation = CirculationSerializer()
    client = ClientSerializer()

    class Meta:
        model = Message
        fields = '__all__'
