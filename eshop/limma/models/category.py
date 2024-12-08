from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=30)
    def __str__(self):
        return self.name
    @staticmethod
    def get_allcategories():

        return Category.objects.all()