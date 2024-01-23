import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from tables.models import Filter, Tag


SOURCE_MODEL = {
    'data/filters.csv': Filter,
    'data/tags.csv': Tag,
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        for source, model in SOURCE_MODEL.items():
            with open(settings.BASE_DIR / source, 'r', encoding='utf-8') as f:
                csvreader = csv.reader(f)
                next(csvreader)
                object_list = []
                for row in csvreader:
                    object_list.append(model(name=row[0]))
                model.objects.bulk_create(object_list)
