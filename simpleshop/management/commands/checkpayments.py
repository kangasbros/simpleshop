import datetime
from django.core.management.base import BaseCommand, CommandError
from simpleshop.models import *

class Command(BaseCommand):
    help = 'Checks if payments have been made, and prunes old orders.'
    
    def handle(self, *args, **options):
        # Execute command on all orders marked unpaid
        orders = Purchase.objects.filter(paid_at=None)
        for order in orders:
            order.check_payment_status()
        
        # Execute on all unpaid orders older than 14 days
        # TODO: Set to variable prune time
        orders = Purchase.objects.filter(paid_at=None, created_at__lte=(datetime.datetime.now()-datetime.timedelta(days=14)))
        for order in orders:
            order.prune()

