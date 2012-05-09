import json
import urllib
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from decimal import Decimal
from currency import currency2btc

BITCOIN_CONFIRMATIONS_REQUIRED = getattr(
    settings, 
    "BITCOIN_CONFIRMATIONS_REQUIRED", 
    2)

BITCOIN_FIAT_CURRENCY = getattr(
    settings, 
    "BITCOIN_FIAT_CURRENCY", 
    "USD")

SHOP_NAME = getattr(
    settings, 
    "SHOP_NAME", 
    "Bitcoin2PirateBox.com")

SHOP_CONFIRMATION_MESSAGE_SUBJECT = getattr(
    settings, 
    "SHOP_CONFIRMATION_MESSAGE_SUBJECT", 
    "Your Bitcoin2PirateBox.com purchase and payment has been confirmed!")

SHOP_CONFIRMATION_MESSAGE = getattr(
    settings, 
    "SHOP_CONFIRMATION_MESSAGE", 
    """
Thanks for shopping at Bitcoin2PirateBox.com!

Your purchase and payment confirmed successfully. We will ship your product(s) ASAP.
Check your purchase information below. If anything is wrong, contact use ASAP!
""")

SHOP_PRUNED_ORDER_SUBJECT = getattr(
    settings,
    "SHOP_PRUNED_SUBJECT",
    "Your Bitcoin2PirateBox.com order has been deleted.")

SHOP_PRUNED_ORDER_MESSAGE = getattr(
    settings,
    "SHOP_PRUNED_ORDER_MESSAGE",
    """
We are sending you this email as we regret to inform you that your order has been deleted from our servers.

You did not send payment within the required timeframe, and as such we have removed your order from our database.

If you are still interested in our products, we invite you to visit us again at http://www.Bitcoin2PirateBox.com/
""")

SHOP_FROM_EMAIL = getattr(
    settings, 
    "SHOP_FROM_EMAIL", 
    "support@Bitcoin2PirateBox.com")

class BitcoinAddress(models.Model):
    address = models.CharField(max_length=36)
    received_least = models.DecimalField(max_digits=16, decimal_places=8, default=Decimal(0))
    used = models.BooleanField(default=False)

    def received(self):
        url = "http://blockchain.info/q/addressbalance/" + self.address + "?confirmations=" + str(BITCOIN_CONFIRMATIONS_REQUIRED)
        f = urllib.urlopen(url, None)
        data = f.read()
        r = Decimal(data) * Decimal("0.00000001")
        if r > self.received_least:
            self.received_least = r
            self.save()
        return r
    
    def __unicode__(self):
        return self.address
        
class Product(models.Model):
    name = models.CharField(max_length=200)
    image_url = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=None)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    
    def __unicode__(self):
        return self.name
        
class Purchase(models.Model):
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, default=None)
    shipped_at = models.DateTimeField(blank=True, default=None)
    
    bitcoin_address = models.OneToOneField("BitcoinAddress")
    bitcoin_payment = models.DecimalField(max_digits=16, decimal_places=8, default=None)
    price_total = models.DecimalField(max_digits=8, decimal_places=2, default=None)
    products = models.ManyToManyField("Product", through='ProductPurchase')
    
    name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()
    
    def check_payment_status(self):
        if not self.bitcoin_payment:
            raise Exception("total price not calculated")
        if self.paid_at:
            return True
        if self.bitcoin_address.received() >= self.bitcoin_payment:
            self.paid_at = timezone.now()
            list_products = "Products\n----------\n"
            for pp in ProductPurchase.objects.filter(purchase=self):
                list_products += pp.product.name + ", " + str(pp.product.price) + " " + BITCOIN_FIAT_CURRENCY + " x " + str(pp.count) + "\n"
            list_products += "----------\n"
            list_products += "Total: " + str(self.price_total) + BITCOIN_FIAT_CURRENCY + "\n"
            list_products += "Paid in bitcoins: " + str(self.bitcoin_payment) + " BTC\n\n"
            list_products += "Email: " + self.email + "\n"
            list_products += "Shipping address:\n" + self.name + "\n" + self.address + "\n"
            send_mail(SHOP_CONFIRMATION_MESSAGE_SUBJECT, SHOP_CONFIRMATION_MESSAGE + "\n\n" + list_products, SHOP_FROM_EMAIL, [self.email],
                fail_silently=False)
            send_mail('New order received', list_products, self.email, [SHOP_FROM_EMAIL],
                fail_silently=False)
            self.save()
            return True
        return False
    
    def prune(self):
        self.bitcoin_address.used = False
        self.bitcoin_address.save()
        
        for pp in ProductPurchase.objects.filter(purchase=self):
            pp.delete()
        
        send_mail(SHOP_PRUNED_ORDER_SUBJECT, SHOP_PRUNED_ORDER_MESSAGE, SHOP_FROM_EMAIL, [self.email],
            fail_silently=False)
        
        self.delete()
    
    def finalize_order(self):
        if self.price_total:
            raise Exception("should do finalize_order only once")
        total = Decimal(0)
        for pp in ProductPurchase.objects.filter(purchase=self):
            total += pp.count * pp.product.price
        self.price_total = total
        self.bitcoin_payment = currency2btc(self.price_total, BITCOIN_FIAT_CURRENCY)
        self.save()
        
        self.bitcoin_address.used = True
        self.bitcoin_address.save()
        
        return True

class ProductPurchase(models.Model):
    product = models.ForeignKey(Product)
    purchase = models.ForeignKey(Purchase)
    count = models.PositiveIntegerField()
