from django.shortcuts import render_to_response
from simpleshop.models import *
from simpleshop.forms import PurchaseForm
from simpleshop import currency

def index(request):
    # Check if the user has submitted the order form.
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        # If the form's valid, process the order.
        if form.is_valid():
            # Find an unused bitcoin address
            bitcoinaddress = BitcoinAddress.objects.filter(used=False)[:1][0]
            
            # Save the information to the database
            # Currently just using one product
            purchase = Purchase.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                address=request.POST.get('address'),
                bitcoin_address=bitcoinaddress)
            product = Product.objects.all()[:1][0]
            pp = ProductPurchase.objects.create(
                product=product,
                purchase=purchase,
                count=request.POST.get('quantity'))
            pp.save()
            
            # Finalize order (get price, mark address used)
            purchase.finalize_order()
            
            # Show them an adress to send money to.
            return render_to_response('payment.html', {
                'shop_name': SHOP_NAME,
                'shop_email': SHOP_FROM_EMAIL,
                'cost': purchase.bitcoin_payment,
                'bitcoin_address': bitcoinaddress,
                'email_address': request.POST.get('email'),
            })
        # The form isn't valid, so we return an error.
        else:
            return render_to_response('index.html', {
                'form': form,
                'error_message': 'Please fill out the form correctly and try again.',
            })
    
    # If we get to this point, the user hasn't submitted the form, so display it.
    form = PurchaseForm()
    return render_to_response('index.html', {'form': form})
    
