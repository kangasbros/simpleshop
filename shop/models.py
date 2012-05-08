from django.db import models

# Create your models here.


class BitcoinAddress(models.Model):
	"""A bitcoin address which can receive bitcoins"""
	
	created_at = models.DateTimeField(blank=True, default=datetime.datetime.now)
	address = models.CharField(blank=True, max_length=100)
	at_use = models.BooleanField(default=False)
	