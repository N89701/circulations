from celery import shared_task
from django.db.models import Q
from django.utils import timezone


@shared_task
def send_messages(circulation_id):
    """Отложенная задача по извлечению объекта рассылки, фильтрации
    пользователей согласно указанным фильтрам и созданию сообщений в БД"""
    from tables.models import Circulation, CirculationFilter, Client, Message
    try:
        circulation = Circulation.objects.get(id=circulation_id)
        filters = circulation.circulationfilter_set.all()
        query = Q()
        for filter in filters:
            if filter.filter.pk == 1:
                query &= Q(operatore_code=filter.value)
            else:
                query &= Q(tags__name=filter.value)
        clients = Client.objects.filter(query).prefetch_related('tags')
        if circulation.endtime is None or timezone.now() < circulation.endtime:
            Message.objects.bulk_create(
                Message(
                    circulation=circulation,
                    client=client,
                    text=circulation.text
                ) for client in clients
            )
    except Circulation.DoesNotExist:
        pass
