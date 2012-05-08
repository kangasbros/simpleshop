from django.db import models

class BitcoinAddress(models.Model):
    address = models.CharField(max_length=36)
    
    def __unicode__(self):
        return self.address
        
class Product(models.Model):
    name = models.CharField(max_length=200)
    image_url = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    
    def __unicode__(self)
        return self.name
        
class Purchase(models.Model):
    bitcoin_address = models.ForeignKey("BitcoinAddress")
    # Not sure how this many-to-many thing will work.
    products = models.ManyToManyField("Product")
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    # Not sure how to do international zip / state / province
    postal_code = models.IntegerField()
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=40)
    
