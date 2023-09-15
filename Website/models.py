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
    mobile = models.CharField(max_length=255,unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    # Other fields for user profile

    def __str__(self):
        return self.user.username

class UserAddress(models.Model):
    user_addr_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)  # Assuming RegisterUser is another model
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)

    def __str__(self):
        return f'User Address for {self.user.email}'

class SellerRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)
    # approved = models.BooleanField(default=False)
    gstin = models.CharField(max_length=15, blank=True)
    document = models.FileField(upload_to='seller_documents/', blank=True)
    company = models.CharField(max_length=100, blank=True,null=True)

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



# product

class ProductCategory(models.Model):
    categ_id = models.AutoField(primary_key=True)  # Use AutoField instead of IntegerField
    categ_name = models.CharField(max_length=255, null=False, unique=True)
    categ_image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.categ_name

class ProductSubcategory(models.Model):
    sub_cat_id = models.AutoField(primary_key=True)
    categ_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    sub_cat_name = models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.sub_cat_name


from django.db import models


class Product(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=255, null=False,unique=True)
    sub_categ_id = models.ForeignKey(ProductSubcategory, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # Use Django's default user model
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prod_name


class ProductDescription(models.Model):
    prod_desc_id = models.AutoField(primary_key=True)
    prod_id = models.OneToOneField(Product, on_delete=models.CASCADE,unique=True)
    description = models.TextField(null=False)
    img1 = models.ImageField(upload_to='product_images/', null=False)
    img2 = models.ImageField(upload_to='product_images/', null=False)
    img3 = models.ImageField(upload_to='product_images/', null=False)
    instructions = models.TextField(null=False)

    def __str__(self):
        return f"Description for {self.prod_id.prod_name}"


class AddCart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)  # Using the User model from Django's auth module
    cart_date = models.DateTimeField(auto_now_add=True) 

class CartItems(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(AddCart, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)  # Assuming you have a Product model
    quantity = models.IntegerField()
    cart_item_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Set a default value of 0.0

    def save(self, *args, **kwargs):
        # Calculate the total price based on the quantity and the price of the associated product
        if self.prod:
            self.total_price = self.quantity * self.prod.price  # Assuming 'price' is a field in your Product model
        super().save(*args, **kwargs)


