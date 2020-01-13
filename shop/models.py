from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from django.utils import timezone

class Item(models.Model):
    categoryChoices = [
        (1, 'Baby'),
        (2, 'Beverages'),
        (3, 'Bread and Bakery'),
        (4, 'Breakfast and Cereal'),
        (5, 'Canned Goods and Soups'),
        (6, 'Condiments/Spices and Bake'),
        (7, 'Cookies, Snacks and Candy'),
        (8, 'Diary, Eggs and Cheese'),
        (9, 'Frozen Foods'),
        (10, 'Produce: Fruits and Vegetables'),
        (11, 'Grains, Pasta and Sides'),
        (12, 'Miscellaneous'),
        (13, 'Paper Products'),
        (14, 'Cleaning Supplies'),
        (15, 'Cosmetics'),
        (16, 'Pet Care'),
        (17, 'Pharmacy')
    ]

    Name = models.CharField(max_length=100)
    Category = models.PositiveSmallIntegerField(default=1 ,choices=categoryChoices)
    Price = models.FloatField(default=100, validators=[MinValueValidator(0.0)])
    Discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    Details = models.TextField(max_length=300)
    Stock = models.PositiveIntegerField(default=500, validators=[MinValueValidator(0)])
    Image = models.ImageField(default="default.jpg", upload_to='item_pics')
    Slug = models.SlugField(default=Name)

    def __str__(self):
        return self.Name + " " + self.Details

    @property
    def FinalPrice(self):
        return self.Price * ((100 - self.Discount) / 100)

    def save(self):
        super().save()

        img = Image.open(self.Image.path)
        if(img.height > 300 or img.width > 300):
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.Image.path)

class Order_Item(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Item = models.ForeignKey(Item, on_delete=models.CASCADE)
    Ordered = models.BooleanField(default=False)
    Quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.Quantity} of {self.Item}"

    @property
    def get_total_item_price(self):
        return self.Quantity * self.Item.FinalPrice

class Address(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Apartment = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    Street = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    Zip = models.CharField(max_length=6, validators=[MinLengthValidator(6)])

    def __str__(self):
        return self.Apartment + ", " + self.Street

class Order(models.Model):
    paymentChoices = [(1, 'Cash on Delivery'), (2, 'Card Payment on Delivery')]

    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Items = models.ManyToManyField(Order_Item)
    OrderDate = models.DateTimeField(default=timezone.now)
    Address = models.ForeignKey(Address, on_delete=models.CASCADE)
    Payment = models.PositiveSmallIntegerField(choices=paymentChoices, default=1)
    Delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.User.username

    @property
    def get_total(self):
        total = 0
        for orderItem in self.Items.all():
            total += orderItem.get_total_item_price
        return total