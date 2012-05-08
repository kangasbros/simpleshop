from django.shortcuts import render_to_response
from simpleshop.models import Product

def index(request):
    product_list = Product.objects.all().order_by('price')
    return render_to_response('simpleshop/index.html', {'product_list': product_list})
