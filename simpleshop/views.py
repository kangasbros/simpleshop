from django.shortcuts import render_to_response
from django.core.mail import send_mail
from simpleshop.models import *
from simpleshop.forms import PurchaseForm
from simpleshop import currency

def index(request):
    # TODO: Add support for multiple products.
    products = Product.objects.all()
    if products.count() != 1 or products[0].stock <= 0:
        return render_to_response('index.html', {
            'out_of_stock': True,
        })

    # Check if the user has submitted the order form.
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        # If the form's valid, process the order.
        if form.is_valid():
            # Find an unused bitcoin address
            unused_bc_addresses = BitcoinAddress.objects.filter(used=False)[:100]
            if not unused_bc_addresses:
                return render_to_response('index.html', {
                    'form': form,
                    'error_message': 'We seem to have run out of Bitcoin addresses to process your order. Please try again in 10 minutes.',
                })
            if unused_bc_addresses.count() < 100:
                send_mail('Almost out of Bitcoin addresses!',
                    "There are less than 100 Bitcoin addresses left in the database.\n\nThought you'd wanna know!",
                    SHOP_FROM_EMAIL, [SHOP_FROM_EMAIL],
                    fail_silently=True)
            
            bitcoinaddress = unused_bc_addresses[0]
            
            # Save the information to the database
            purchase = Purchase(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                address=request.POST.get('address'),
                bitcoin_address=bitcoinaddress)
            
            purchase.save()
            
            # Connect the purchase to the products
            pp = ProductPurchase.objects.create(
                product=product,
                purchase=purchase,
                count=request.POST.get('quantity'))
            
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
    
