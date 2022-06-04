from django.core.management.base import BaseCommand, CommandError
import json

from housearch.helpers import load_geo_json

class Command(BaseCommand):
    help = 'Load data from territorial geo json'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        with open(options['file']) as f:
            data = json.load(f)
        
        load_geo_json(data, True)

        self.stdout.write(self.style.SUCCESS('Successfully loaded data'))