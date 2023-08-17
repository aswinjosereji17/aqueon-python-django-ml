from django.contrib import admin

# Register your models here.
from .models import UserProfile,SellerRequest,HomeSpecialOffer, ProductCategory, ProductSubcategory, Product

# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'street_address', 'city', 'state', 'postal_code', 'country')
    # Other customization options

# admin.site.register(UserProfile)
# admin.site.register(SellerRequest)
admin.site.register(HomeSpecialOffer)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'profile_image')  

admin.site.register(UserProfile, UserProfileAdmin)

class SellerRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'gstin', 'document')  # Add other fields here

admin.site.register(SellerRequest, SellerRequestAdmin)


admin.site.register(ProductCategory)
admin.site.register(ProductSubcategory)
admin.site.register(Product)
