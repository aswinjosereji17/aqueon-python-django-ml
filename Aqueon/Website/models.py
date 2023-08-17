from django.db import models

# Create your models here.
from django.contrib.auth.models import User

# class UserProfile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     address = models.CharField(max_length=255)
#     # Other fields for user profile

#     def __str__(self):
#         return self.user.username  # Return the username as the string representation
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    # Other fields for user profile

    def __str__(self):
        return self.user.username

class SellerRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # approved = models.BooleanField(default=False)
    gstin = models.CharField(max_length=15, blank=True)
    document = models.FileField(upload_to='seller_documents/', blank=True)

    def __str__(self):
        return self.user.username



class HomeSpecialOffer(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=100)
    description = models.TextField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='special_offer_images/')  # Define the image field

    def __str__(self):
        return self.prod_name

class ProductCategory(models.Model):
    categ_id = models.AutoField(primary_key=True)
    categ_name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.categ_name

class ProductSubcategory(models.Model):
    sub_cat_id = models.AutoField(primary_key=True)
    categ_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    sub_cat_name = models.CharField(max_length=255)

    def __str__(self):
        return self.sub_cat_name

class Product(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=255, null=False)
    sub_categ_id = models.ForeignKey(ProductSubcategory, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.prod_name