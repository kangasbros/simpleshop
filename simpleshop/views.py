from django.shortcuts import render_to_response
from simpleshop.models import *
from simpleshop.forms import PurchaseForm

def index(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            return render_to_response('payment.html', {
                'shop_name': SHOP_NAME,
                'shop_email': SHOP_FROM_EMAIL,
                'bitcoin_address': '1Lauokt6UDNmHLC4RgoSS4Uc7sc6YYjQRn',
                'cost': '20',
                'email_address': 'example@example.com'
            })
        else:
            return render_to_response('index.html', {
                'form': form,
                'error_message': 'Please fill out the form correctly and try again.'
            })

    form = PurchaseForm()
    return render_to_response('index.html', {'form': form})
    
