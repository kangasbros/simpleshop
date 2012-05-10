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

        # TODO: Setup variable prune / reminder time

        # Send a reminder to users with an order older than 1 day
        orders = Order.objects.filter(closed=False, paid_at=None, created_at__lte=(timezone.now()-datetime.timedelta(days=1)))
        for order in orders:
            order.send_reminder()
        
        # Prune all unpaid orders older than 2 days
        orders = Order.objects.filter(closed=False, paid_at=None, created_at__lte=(timezone.now()-datetime.timedelta(days=2)))
        for order in orders:
            order.prune()
