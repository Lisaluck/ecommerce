# Generated by Django 4.2.5 on 2024-10-13 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('limma', '0006_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='cart_images/'),
        ),
    ]
