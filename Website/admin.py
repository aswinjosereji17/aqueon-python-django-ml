from django.contrib import admin

# Register your models here.
from .models import UserProfile,SellerRequest,HomeSpecialOffer,ProductCategory, ProductSubcategory, Product, ProductDescription, UserAddress, AddCart, CartItems, Wishlist
#  ProductCategory, ProductSubcategory, Product
from .models import Review, ProductRequest,Fish,Event
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'street_address', 'city', 'state', 'postal_code', 'country')
    # Other customization options

# admin.site.register(UserProfile)
# admin.site.register(SellerRequest)
admin.site.register(HomeSpecialOffer)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile', 'profile_image')  

admin.site.register(UserProfile, UserProfileAdmin)

class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address1', 'address2')

admin.site.register(UserAddress, UserAddressAdmin)

class SellerRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'gstin', 'document', 'request_time')  # Add other fields here

admin.site.register(SellerRequest, SellerRequestAdmin)

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('categ_id', 'categ_name','created_at')  # Add other fields here

admin.site.register(ProductCategory, ProductCategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('prod_name','fish_name','sub_categ_id','price','user_id','stock_quantity','created_at')  # Add other fields here

admin.site.register(Product, ProductAdmin)

# admin.site.register(ProductCategory)
# admin.site.register(ProductSubcategory)
# admin.site.register(Product)
class ProductDescriptionAdmin(admin.ModelAdmin):
    list_display = ('prod_desc_id','prod_id','description','instructions','img1')  # Add other fields here
admin.site.register(ProductDescription,ProductDescriptionAdmin)

class ProductSubcategoryAdmin(admin.ModelAdmin):
    list_display = ('categ_id','sub_cat_name','created_at')  # Add other fields here

admin.site.register(ProductSubcategory, ProductSubcategoryAdmin)

admin.site.register(AddCart)
admin.site.register(CartItems)
# admin.site.register(Wishlist)

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user_id','wishlist_date','prod_id')  # Add other fields here

admin.site.register(Wishlist, WishlistAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id','user','prod','rating','outof_rating','description','sentiment_score','created_at') 



admin.site.register(Review,ReviewAdmin)
admin.site.register(ProductRequest)

from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Number of empty forms to show for adding related OrderItems

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'order_date', 'razorpay_order_id', 'payment_status']
    inlines = [OrderItemInline]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'total_price']

# Register the models with the admin site
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

admin.site.register(Fish)

class EventAdmin(admin.ModelAdmin):
    list_display = ['event_id','name','event_img', 'date','description', 'mode', 'duration', 'booking_link','created_at']

admin.site.register(Event, EventAdmin)
