from django.contrib import admin
# Register your models here.
from .models.product import Product
from .models.category import Category
from .models.cart import Cart
from .models.customer import Customer
from .models.order import OrderDetail
class AdminProduct(admin.ModelAdmin):
    list_display=['name','price','id','description','category']
class AdminCart(admin.ModelAdmin):
    list_display=['phone','product','id','price','image']
class AdminCustomer(admin.ModelAdmin):
    list_display=['name','id','phone']
class AdminOrder(admin.ModelAdmin):
    list_display=['id','user','product_name','ordered_date','qty','image','price','status']
admin.site.register(Product,AdminProduct)
admin.site.register(Category)
admin.site.register(Customer,AdminCustomer)
admin.site.register(Cart,AdminCart)
admin.site.register(OrderDetail,AdminOrder)