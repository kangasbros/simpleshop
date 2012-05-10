from django.shortcuts import render_to_response
from django.core.mail import send_mail
from simpleshop.models import *
from simpleshop.forms import OrderForm
from simpleshop import currency

def index(request):
    # Check whether any products are even in stock
    # TODO: Add support for multiple products.
    products = Product.objects.all()
    if products.count() != 1 or products[0].stock <= 0:
        return render_to_response('index.html', {
            'out_of_stock': True,
        })
    
    # Check if the user has submitted the order form.
    if request.method == 'POST':
        form = OrderForm(request.POST)
        # If the form's valid, process the order.
        if form.is_valid():
            # Save the information to the database
            order = Order.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                address=request.POST.get('address'))
            
            # Connect the order to the products
            # TODO: Add support for multiple products.
            product = products[0]
            op = OrderProduct.objects.create(
                product=product,
                order=order,
                count=request.POST.get('quantity'))
            
            # Calculate price of the order
            order.calculate_price()
            
            # Show them an adress to send money to.
            return render_to_response('payment.html', {
                'shop_name': SHOP_NAME,
                'shop_email': SHOP_FROM_EMAIL,
                'price': order.bitcoin_payment,
                'bitcoin_address': order.bitcoin_address,
                'email_address': request.POST.get('email'),
            })
        # The form isn't valid, so we return an error.
        return render_to_response('index.html', {
            'form': form,
            'form_error': True,
        })
    
    # If we get to this point, the user hasn't submitted the form, so display it.
    form = OrderForm()
    return render_to_response('index.html', {'form': form})
