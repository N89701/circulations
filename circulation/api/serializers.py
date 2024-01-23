from rest_framework.serializers import (
    DateTimeField, ImageField, IntegerField, ModelSerializer,
    PrimaryKeyRelatedField, ValidationError
)

from tables.models import (
    Circulation, CirculationFilter, Client, Filter, Message, Tag
)


class CirculationFilterCreateSerializer(ModelSerializer):
    filter_id = PrimaryKeyRelatedField(queryset=Filter.objects.all())

    class Meta:
        model = CirculationFilter
        fields = ('filter_id', 'amount')


class CirculationCreateSerializer(ModelSerializer):
    filters = CirculationFilterCreateSerializer(many=True)

    class Meta:
        model = Filter
        fields = '__all__'
