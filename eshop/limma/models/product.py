from django.db import models
from .category import Category

class Product(models.Model):
    name=models.CharField(max_length=600)
    price=models.IntegerField(default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    image=models.ImageField(upload_to='uploadedtoo/products/')
    description=models.CharField(max_length=1000,blank=True)
    @staticmethod
    def get_all_product():
        return Product.objects.all()
    def get_all_product_by_category(Category_id):
        if Category_id:
            return Product.objects.filter(category=Category_id)
        else:
            return Product.get_all_product()
    def __str__(self):
        return self.name

