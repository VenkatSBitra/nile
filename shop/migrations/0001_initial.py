# Generated by Django 3.0 on 2019-12-20 05:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemName', models.CharField(max_length=100)),
                ('itemCategory', models.CharField(choices=[(1, 'Baby'), (2, 'Beverages'), (3, 'Bread and Bakery'), (4, 'Breakfast and Cereal'), (5, 'Canned Goods and Soups'), (6, 'Condiments/Spices and Bake'), (7, 'Cookies, Snacks and Candy'), (8, 'Diary, Eggs and Cheese'), (9, 'Frozen Foods'), (10, 'Produce: Fruits and Vegetables'), (11, 'Grains, Pasta and Sides'), (12, 'Miscellaneous'), (13, 'Paper Products'), (14, 'Cleaning Supplies'), (15, 'Cosmetics'), (16, 'Pet Care'), (17, 'Pharmacy')], max_length=100)),
                ('itemPrice', models.PositiveIntegerField(default=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('itemDiscount', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('itemDetails', models.TextField(max_length=300)),
                ('itemStock', models.PositiveIntegerField(default=500, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
    ]