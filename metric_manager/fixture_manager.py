from .models import *
from django.core.management import call_command

def load_fixtures():
    if len(MetricsDescription.objects.all())==0:
        call_command('loaddata', 'metric_manager/fixtures/fixtures.json')
