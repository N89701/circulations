from datetime import datetime, timedelta

from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils import timezone

from celery_app.tasks import send_messages
from tables.validators import numeric_only, validate_telephone_number




class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Filter(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Circulation(models.Model):
    time = models.DateTimeField(
        default=now,
        blank=True
    )
    text = models.TextField()
    filters = models.ManyToManyField(
        Filter,
        through='CirculationFilter',
        blank=True,
    )
    endtime = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.time.timestamp() > datetime.now().timestamp()-30:
            send_messages.apply_async((self.id,), eta=self.time)


class CirculationFilter(models.Model):
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
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
    tags = models.ManyToManyField(
        Tag,
        blank=True,
    )


class Message(models.Model):
    sending_time = models.DateTimeField(auto_now_add=True)
    circulation = models.ForeignKey(
        Circulation,
        null=True,
        on_delete=models.SET_NULL,
        related_name='messages'
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    text = models.TextField()
