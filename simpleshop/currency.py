# -*- coding: utf-8 -*-
"""Usage:
"""

import decimal

from django.core.cache import cache

import json
import sys
import urllib
import urllib2
import random
import hashlib
import base64
from decimal import Decimal
import decimal
import warnings

# simple utility functions for conversions

CURRENCY_CHOICES = (
    ('BTC', 'BTC'),
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('AUD', 'AUD'),
    ('BRL', 'BRL'),
    ('CAD', 'CAD'),
    ('CHF', 'CHF'),
    ('CNY', 'CNY'),
    ('DKK', 'DKK'),
    ('GBP', 'GBP'),
    ('HKD', 'HKD'),
    ('JPY', 'JPY'),
    ('NZD', 'NZD'),
    ('PLN', 'PLN'),
    ('RUB', 'RUB'),
    ('SEK', 'SEK'),
    ('SLL', 'SLL'),
)

RATE_PERIOD_CHOICES=("24h", "7d", "30d",)

def get_rate_table():
    cache_key="bitcoincharts_all"
    cache_key_old="bitcoincharts_all_old"
    if not cache.get(cache_key):
        try:
            f = urllib2.urlopen(
                u"http://bitcoincharts.com/t/weighted_prices.json")
            result=f.read()
            j=json.loads(result)
            cache.set(cache_key, j, 60*60)
            print result
        except:
            print "Unexpected error:", sys.exc_info()[0]

        if not cache.get(cache_key):
            if not cache.get(cache_key_old):
                raise TemporaryConversionError(
                    "Cache not enabled, reliable exchange rate is not available")
            cache.set(cache_key, cache.get(cache_key_old), 60*60)

        cache.set(cache_key_old, cache.get(cache_key), 60*60*24*7)
    return cache.get(cache_key)

def currency_list():
    return get_rate_table().keys()

def get_currency_rate(currency="USD", rate_period="24h"):
    try:
        return Decimal(get_rate_table()[currency][rate_period])
    except KeyError:
        return None

def btc2currency(amount, currency="USD", rate_period="24h"):
    rate=get_currency_rate(currency, rate_period)
    if rate==None:
        return None
    return (amount*rate).quantize(Decimal("0.01"))

def currency2btc(amount, currency="USD", rate_period="24h"):
    rate=get_currency_rate(currency, rate_period)
    if rate==None:
        return None
    return (amount/rate).quantize(Decimal("0.00000001"))


