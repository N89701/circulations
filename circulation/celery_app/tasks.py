from celery import shared_task
from django.utils import timezone


@shared_task
def send_messages(circulation_id):
    from tables.models import Circulation, CirculationFilter, Client, Message
    try:
        circulation = Circulation.objects.get(id=circulation_id)

        circulation_filters = CirculationFilter.objects.filter(
            circulation=circulation
        )
        clients = Client.objects.all().prefetch_related('tags')
        for filter in circulation_filters:
            filter_value = filter.value
            if filter.filter.pk == 1:
                clients = Client.objects.filter(operatore_code=filter_value)
            else:
                clients = Client.objects.filter(tags__name=filter_value)

        for client in clients:
            if circulation.endtime is not None:
                deadline = circulation.endtime
                for client in clients:
                    if timezone.now() < deadline:
                        Message.objects.create(
                            circulation=circulation,
                            client=client,
                            text=circulation.text
                        )
            else:
                for client in clients:
                    Message.objects.create(
                        circulation=circulation,
                        client=client,
                        text=circulation.text
                    )
    except Circulation.DoesNotExist:
        pass
