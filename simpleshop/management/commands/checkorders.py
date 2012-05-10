import datetime
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from simpleshop.models import *

class Command(BaseCommand):
    help = 'Checks if payments have been made, and prunes old orders.'
    
    def handle(self, *args, **options):
        # Execute command on all orders marked unpaid
        orders = Order.objects.filter(paid_at=None)
        for order in orders:
            order.check_payment_status()
        
        # Execute on all unpaid orders older than a day
        # TODO: Set to variable prune time
        orders = Order.objects.filter(paid_at=None, created_at__lte=(timezone.now()-datetime.timedelta(days=1)))
        for order in orders:
            order.prune()

