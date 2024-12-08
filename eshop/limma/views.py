from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models.product import Product
from .models.customer import Customer
from .models.category import Category
from django.http import JsonResponse
from .models.cart import Cart
from django.contrib import messages
from django.views import View
from django.db.models import   Q
from .models.order import OrderDetail

def home(request):
    products=None
    totalitem=0
    if request.session.has_key('phone'):
        phone=request.session['phone']
        category=Category.get_allcategories()
        customer=Customer.objects.filter(phone=phone)
        totalitem=len(Cart.objects.filter(phone=phone))
        for c in customer:
            name=c.name
            categoryId = request.GET.get('category')
            if categoryId:
                products = Product.get_all_product_by_category(categoryId)
            else:

                products = Product.get_all_product()

                data = {}

                data['name'] = name
                data['products'] = products
                data['category'] = category
                data['totalitem']=totalitem
                return render(request, 'limma/home.html'
                              , data)

    else:
        return redirect('login')


class Signup(View):
    def get(self,request):
        if request.method == 'GET':
            return render(request, 'limma/signup.html')
    def post(self,request):
        postData=request.POST
        name=postData.get("name")
        phone=postData.get("mobile")
        customer=Customer(name=name,phone=phone)
        error_message= None
        value={
            'phone':phone,
            'name':name
        }
        if(not name):

            error_message="name is required,enter the name "
        elif  not phone:
            error_message="phone  number is required "
        elif len(phone)<10:
            error_message="phone number must be of 10 character long or more "
        elif customer.isExists():

            error_message="customer is already registered with this number"
        if not error_message:

            messages.success(request,'congratulation !! register successful')
            customer.register()
            return redirect('signup')
        else:
            data={
                'error':error_message,
                'value':value
            }
            return render(request,'limma/signup.html',data)
class Login(View):
    def get(self,request):
        return render(request,'limma/login.html')
    def post(self,request):
        phone = request.POST.get('phone')
        error_message = None
        customer = Customer.objects.filter(phone=request.POST["phone"])
        if  customer:
            request.session['phone']=phone
        if customer.exists():  # Check if the customer exists
            return redirect('homepage')
        else:
            error_message = "Mobile number is invalid"

        return render(request, 'limma/login.html', {'error': error_message})
def productdetail(request,pk):
    product=Product.objects.get(pk=pk)
    item_already_in_cart=False
    if request.session.has_key('phone'):
        phone=request.session['phone']
        totalitem=len(Cart.objects.filter(phone=phone))
        item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(phone=phone)).exists()
        customer=Customer.objects.filter(phone=phone)
        for c in customer:
            name=c.name

        data={
            'product':product,
            'item_already_in_cart':item_already_in_cart,
            'name':name,
            'totalitem': totalitem
        }
    return render(request,'limma/productdetail.html',data)
def logout(request):
    if request.session.has_key('phone'):
        del request.session['phone']
        return redirect('login')
    else:
        return redirect('login')
def add_to_cart(request):
    phone = request.session.get('phone', None)
    if not phone:
        return redirect('login')  # Redirect to login if phone is not in session

    product_id = request.GET.get('prod_id')
    try:
        product = Product.objects.get(id=product_id)  # Get the product by ID

        # Create and save Cart object
        cart_item = Cart(
            phone=phone,
            product=product,
            image=product.image,  # Use the product's image directly
            price=product.price
        )
        cart_item.save()

        return redirect(f"/product-detail/{product_id}")  # Redirect to product detail page
    except Product.DoesNotExist:
        return redirect('homepage')  # If product doesn't exist, redirect to homepage

def show_cart(request):
    totalitem=0
    if request.session.has_key('phone'):
        phone=request.session['phone']
        totalitem=len(Cart.objects.filter(phone=phone))
        customer = Customer.objects.filter(phone=phone)
        for c in customer:
            name = c.name
            cart = Cart.objects.filter(phone=phone)
            data={
                'name':name,
                'totalitem':totalitem,
                'cart':cart
            }
            if cart:
                return render(request,'limma/show_cart.html',data)
            else:
                return render(request,'limma/empty_cart.html')

def plus_cart(request):
    if request.session.has_key('phone'):
        phone=request.session['phone']
        product_id=request.GET['prod_id']
        cart=Cart.objects.get(Q(product_id=product_id)& Q(phone=phone))
        cart.quantity+=1
        cart.save()
        data={
                'quantity':cart.quantity
        }
        return JsonResponse(data)
def minus_cart(request):
    if request.session.has_key('phone'):
        phone=request.session['phone']
        product_id=request.GET['prod_id']
        cart=Cart.objects.get(Q(product_id=product_id)& Q(phone=phone))
        cart.quantity-=1
        cart.save()
        data={
                'quantity':cart.quantity
        }
        return JsonResponse(data)
def remove_cart(request):
    if request.session.has_key('phone'):
        phone=request.session['phone']
        product_id=request.GET['prod_id']
        cart=Cart.objects.get(Q(product_id=product_id)& Q(phone=phone))
        cart.delete()
        return JsonResponse()
def checkout(request):
    if request.session.has_key('phone'):
        # Correctly fetch session data
        phone = request.session.get('phone')

        # Fetch data from the POST request
        name = request.POST.get('name')  # Correct key for 'name'
        address = request.POST.get('address')  # Correct key for 'address'
        mobile = request.POST.get('mobile')  # Correct key for 'mobile'

        # Fetch all cart products for the user
        cart_products = Cart.objects.filter(phone=phone)

        # If the cart is empty, handle gracefully
        if not cart_products.exists():
            return render(request, 'limma/empty_cart.html', {'name': 'Guest', 'totalitem': 0})

        # Create orders for each product in the cart
        for c in cart_products:
            OrderDetail.objects.create(
                user=phone,
                product_name=c.product,
                image=c.image,
                qty=c.quantity,
                price=c.price
            )

        # Clear the cart after saving orders
        cart_products.delete()

        # Fetch total items in the cart and customer name
        totalitem = 0  # Cart is empty now
        customer = Customer.objects.filter(phone=phone).first()
        customer_name = customer.name if customer else "Guest"

        # Prepare data for rendering
        data = {
            'name': customer_name,
            'totalitem': totalitem
        }

        # Render the empty cart page
        return render(request, 'limma/empty_cart.html', data)
    else:
        # Redirect to login if the session is not set
        return redirect('login')
def order(request):
    totalitem=0
    if request.session.has_key('phone'):
        phone=request.session["phone"]
        totalitem=len(Cart.objects.filter(phone=phone))
        customer=Customer.objects.filter(phone=phone)
        for c in customer:
            name=c.name
            order = OrderDetail.objects.filter(user=phone)
            data = {
                'order': order,
                'name':name,

                'totalitem':totalitem
            }
            if order:
                return render(request,'limma/order.html',data)
            else:
                return render(request,'limma/emptyorder.html',data)
    else:
        return redirect('login')

def search(request):
    totalitem = 0
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        query=request.GET.get('query')
        search=Product.objects.filter(name__contains=query)
        category=Category.get_allcategories()
        totalitem = len(Cart.objects.filter(phone=phone))
        customer = Customer.objects.filter(phone=phone)
        for c in customer:
            name = c.name
        data={
            'name':name,
            'totalitem':totalitem,
            'search':search,
            'category':category,
            'query':query}
        return render(request,'limma/search.html',data)
    else:
        return redirect('login')