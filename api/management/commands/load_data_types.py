import json
from django.core.management.base import BaseCommand
from api.models import DataType
from api.utils import get_data_types

class Command(BaseCommand):
    help = 'Loads Data Types from generated JSON.'

    def handle(self, *args, **options):
        
        data_types = get_data_types()

        for data_type_data in data_types:
            DataType.objects.create(**data_type_data)

        self.stdout.write(self.style.SUCCESS('Success loading data types.'))