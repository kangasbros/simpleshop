import datetime
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from simpleshop.models import *

class Command(BaseCommand):
    help = 'Checks if payments have been made, and prunes unpaid orders older than a day.'
    
    def handle(self, *args, **options):
        # Check if payment received on all open orders marked unpaid
        orders = Order.objects.filter(closed=False, paid_at=None)
        for order in orders:
            order.check_payment()
        
        # Prune all unpaid orders older than a day
        # TODO: Set to variable prune time
        orders = Order.objects.filter(closed=False, paid_at=None, created_at__lte=(timezone.now()-datetime.timedelta(days=1)))
        for order in orders:
            order.prune()

