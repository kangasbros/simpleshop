from django.db import models


class BitcoinAddress(models.Model):
    address = models.CharField(max_length=36)
    used = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.address
        
class Product(models.Model):
    name = models.CharField(max_length=200)
    image_url = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    
    def __unicode__(self):
        return self.name
        
class Purchase(models.Model):
	created_at = models.DateTimeField(blank=True, default=datetime.datetime.now)
	paid_at = models.DateTimeField(null=True, blank=True, default=None)
	shipped_at = models.DateTimeField(nullTrue, blank=True, default=None)

    bitcoin_address = models.OneToOneField("BitcoinAddress")

    # Not sure how this many-to-many thing will work.
    products = models.ManyToManyField("Product", through='ProductPurchase')
    address = models.TextField(blank=True)

class ProductPurchase(models.Model):
	product = models.ForeignKey(Product)
    purchase = models.ForeignKey(Purchase)
	count = models.IntegerField(blank=True, null=True)
