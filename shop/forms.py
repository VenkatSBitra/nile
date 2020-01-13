from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class ItemSearchForm(forms.Form):
    categoryChoices = [
        (18, 'All'),
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

    name = forms.CharField(max_length=200, required=False)
    category = forms.ChoiceField(choices=categoryChoices)
    min_price = forms.IntegerField(required=False, validators=[MinValueValidator(0)])
    max_price = forms.IntegerField(required=False, validators=[MinValueValidator(min_price)])
    min_discount = forms.IntegerField(required=False, validators=[MinValueValidator(0), MaxValueValidator(100)])


