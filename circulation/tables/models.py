from django.core.validators import MinLengthValidator
from django.db import models

from tables.validators import numeric_only, validate_telephone_number


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Filter(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Circulation(models.Model):
    time = models.DateTimeField(auto_now_add=True, blank=True)
    text = models.TextField()
    filters = models.ManyToManyField(
        Filter,
        through='CirculationFilter',
        blank=True,
        null=True
    )
    endtime = models.DateTimeField(blank=True, null=True)


class CirculationFilter(models.Model):
    filter_name = models.ForeignKey(Filter, on_delete=models.CASCADE)
    circulation = models.ForeignKey(Circulation, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)


class Client(models.Model):
    telephone = models.CharField(
        validators=[validate_telephone_number,],
        max_length=17,
        blank=True,
        unique=True
    )
    operatore_code = models.CharField(
        max_length=3,
        validators=[MinLengthValidator(3), numeric_only]
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )


class Message(models.Model):
    sending_time = models.DateTimeField()
    circulation = models.ForeignKey(
        Circulation,
        null=True,
        on_delete=models.SET_NULL
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
