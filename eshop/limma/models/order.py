from django.db import models
STATUS_CHOICE=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('on the way','on the way'),
    ('Delivered','Delivered'),
    ('cancel','cancel'),

)
class OrderDetail(models.Model):
    user=models.IntegerField(default=True)
    product_name=models.CharField(max_length=250)
    image=models.ImageField(null=True,blank=True)
    qty=models.PositiveIntegerField(default=1)
    price=models.IntegerField()
    ordered_date=models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=50,default='pending',choices=STATUS_CHOICE)

    def __str__(self):
        return f"Order({self.product_name}, {self.status})"