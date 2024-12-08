from django.db import models
class Customer(models.Model):
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=50)
    def register(self):
        self.save()
    def __str__(self):
        return self.name
    def isExists(self):
        if Customer.objects.filter(phone=self.phone):
            return True
        else:
            return False