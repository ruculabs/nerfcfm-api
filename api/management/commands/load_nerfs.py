import json
from django.core.management.base import BaseCommand
from api.models import Nerf
from api.utils import get_nerfs

class Command(BaseCommand):
    help = 'Loads Nerfs from generated JSON.'

    def handle(self, *args, **options):
        
        nerfs = get_nerfs()

        for nerf_data in nerfs:
            Nerf.objects.create(**nerf_data)

        self.stdout.write(self.style.SUCCESS('Success loading nerf data.'))

