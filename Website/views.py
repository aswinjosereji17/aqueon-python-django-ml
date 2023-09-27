from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import UserProfile, Product, SellerRequest, HomeSpecialOffer, ProductCategory,UserAddress, Wishlist
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.cache import never_cache




# Create your views here.
@never_cache
def index(request):


    
    homeimg = HomeSpecialOffer.objects.all()  # Get all events from the database
    prod_cat = ProductCategory.objects.all()
    recent_products = Product.objects.all().order_by('-created_at')[:8]
    
    if request.user.is_authenticated:
        user=request.user
        # homeimg = HomeSpecialOffer.objects.all()  # Get all events from the database
        # prod_cat = ProductCategory.objects.all()
        # return redirect('index')
        try:
            cart = AddCart.objects.get(user=user)
            cart_items = CartItems.objects.filter(cart=cart)
            cart_item_count = cart_items.count()
            user_id = request.user.id  # Use the user's ID if they are logged in
            wish_count = Wishlist.objects.filter(user_id=user_id).count()
        except AddCart.DoesNotExist:
            cart = None
            cart_items = []
            cart_item_count = 0
            wish_count = 0 

        context = {
        'cart' : cart,
        'cart_items' : cart_items,
        'homeimg': homeimg,
        'prod_cat':prod_cat,
        'cart_item_count': cart_item_count,
        'recent_products': recent_products,
        'wish_count' : wish_count
        }
        
        return render(request,'index.html', context)
    else:
        # homeimg = HomeSpecialOffer.objects.all()  # Get all events from the database
        # prod_cat = ProductCategory.objects.all()
        context = {
        'homeimg': homeimg,
        'prod_cat':prod_cat,
        'recent_products': recent_products
        }
        
        return render(request,'index.html', context)
    
@never_cache
def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username_or_email = request.POST['username']
        password = request.POST['password']
        # print("Received username or email:", username_or_email)
        # print("Received password:", password)
        
        if "@" in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                user = None
        else:
            user = authenticate(username=username_or_email, password=password)
            
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, "Invalid Login")
            error_message = "Invalid Login "
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


# def save_google_email(user, backend, response, *args, **kwargs):
#     if backend.name == 'google-oauth2':
#         email = response.get('email')
#         if email and not user.email:
#             user.email = email
#             user.save()


@never_cache  
def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.info(request,"Username Already Exists")
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request,"Email Already Exists") 
            return redirect('register')
        else:
            user=User.objects.create_user(username=username,email=email,password=password)
            user.save()
            # UserProfile.objects.create(user=user, mobile="")
            # UserAddress.objects.create(user=user,address1="",address2="")
            success_message = "Registration successful. You can now log in."
            messages.success(request, success_message)
            return redirect('login_user')
           
    else:
        return render (request, "register.html")

@never_cache
def seller_register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username Already Exists")
            return redirect('seller_register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, "Email Already Exists")
            return redirect('seller_register')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            # user.save()
            company=request.POST['company']
            gstin = request.POST['gstin']
            document = request.FILES.get('document')
            seller_request = SellerRequest.objects.create(user=user,company=company, gstin=gstin, document=document)
            success_message = "Seller request submitted. Please wait for approval."
            # UserProfile.objects.create(user=user, mobile="")
            # UserAddress.objects.create(user=user,address1="",address2="")  
            user.save()
         
            return redirect('login_user')
           
    else:
        return render(request, "seller_reg.html")

@login_required
@never_cache

def loggout(request):
    # print('Logged Out')
    logout(request)
    return redirect('index')


from django.shortcuts import render
from .models import UserProfile,Product, ProductSubcategory, UserAddress, Product
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Count
import datetime
from django.db import models 
from django.views.decorators.cache import never_cache

# def user_profile_view(request):
#     user_profile = UserProfile.objects.get(user=request.user)
    
#     context = {
#         'user_profile': user_profile,
#     }
#     return render(request, 'user_profile.html', context)
@login_required
@never_cache
def user_profile_view(request):

    if not request.user.is_authenticated:
        return redirect('login_user')
    # user_profile = UserProfile.objects.get(user=request.user)
    user_count = User.objects.filter(is_staff=False).count()
    seller_count = User.objects.filter(Q(is_staff=True) & Q(is_superuser=False)).count()
    prod_count = Product.objects.count()
    s_req= SellerRequest.objects.all()


    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None

    # try:
    #     product = Product.objects.filter(user_id=request.user)
    # except Product.DoesNotExist:
    #     product = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    
    context = {
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
        'user_count' : user_count,
        'seller_count' : seller_count,
        'prod_count' : prod_count,
        's_req' : s_req,
        # 'product' :product
    }
    
    return render(request, 'user_prof.html', context)


from django.shortcuts import render, redirect
from .models import UserProfile, UserAddress,SellerRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


# 4-09-2023
@login_required
@never_cache
def edit_profile(request):
    if request.method == 'POST':
        # Get the current user's profile
        user_profile = UserProfile.objects.get(user=request.user)
        user = User.objects.get(username=request.user)
        user_addr= UserAddress.objects.get(user=request.user)

        # Update the profile fields with the submitted form data
        # user_profile.mobile = request.POST.get('mobile')
        # user_profile.save()
        # user_profile.profile_image=request.POST.get('prof_image')
        uploaded_image = request.FILES.get('img1')

        if uploaded_image:
            # Update the user's profile image
            user_profile.profile_image = uploaded_image
        
        user_profile.save()
        

        user_addr.address1=request.POST.get('address1')
        user_addr.address2=request.POST.get('address2')
        user_addr.save()

        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        # user.email=request.POST.get('email')
        user.save()

        # seller_req.company=request.POST.get('company')
        # seller_req.save()
        if request.user.is_staff and not request.user.is_superuser :
            # Get or create a SellerRequest object
            seller_req=SellerRequest.objects.get(user=request.user)
            seller_req.company = request.POST.get('company')
            seller_req.save()  
        # if 'profile_image' in request.FILES:
        #     user_profile.profile_image = request.FILES['profile_image']
        #     user_profile.save()

        
        # Redirect to a success page or profile page
        # return redirect('user_profile_view')
        # show_main2 = True

    # Redirect to 'user_profile_view' with the context variable
        # return render(request, 'user_prof.html', {'show_main2': show_main2})

        return redirect('user_profile')

    # If the request method is GET, render the edit profile form
 


# @login_required
# def create_product(request):
#     if request.method == 'POST':
#         prod_name = request.POST.get('prod_name')
#         sub_categ_id = request.POST.get('sub_categ_id')  # Assuming you get subcategory ID from the form
#         price = request.POST.get('price')

#         # Get the currently logged-in user
#         user = request.user

#         # Create a new product with the logged-in user
#         product = Product(
#             prod_name=prod_name,
#             sub_categ_id=sub_categ_id,
#             price=price,
#             user_id=user
#         )
#         product.save()

#         return redirect('product_list')  # Redirect to a product list view

#     return render(request, 'create_product.html')


# product



# def product_list(request):
#     query = request.GET.get('q')
#     products = Product.objects.filter(user_id=request.user)

#     if query:
#         products = products.filter(Q(prod_name__icontains=query))

#     return render(request, 'user_prof.html', {'products': products, 'query': query})





# product

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductSubcategory, ProductDescription

@login_required
@never_cache

def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.filter(user_id=request.user)
    user_profile = UserProfile.objects.get(user=request.user)
    seller_request = SellerRequest.objects.get(user=request.user)
    user_addr = UserAddress.objects.get(user=request.user)

    if query:
        products = products.filter(Q(prod_name__icontains=query))

    return render(request, 'product\product_list.html', {'products': products, 'query': query , 'user_profile': user_profile, 'seller_request': seller_request,'user_addr' : user_addr})



from django.db import IntegrityError

@login_required
@never_cache
def add_product(request):
    users = User.objects.all()
    seller_requests = SellerRequest.objects.all()
    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    subcategories = ProductSubcategory.objects.all()

    context = {
        'users': users,
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
        'seller_requests' : seller_requests,
        'subcategories': subcategories
    }

    if request.method == 'POST':
        product_name = request.POST['product_name']
        subcategory_id = request.POST['subcategory']
        price = request.POST['price']
        quantity=request.POST['quantity']
        description = request.POST['description']
        instruction = request.POST['instruction']
        img1 = request.FILES['img1']
        img2 = request.FILES['img2']
        img3 = request.FILES['img3']

        # Check if the product name already exists
        if Product.objects.filter(prod_name=product_name).exists():
            # Handle the case where the product name already exists
            return HttpResponse("Product with this name already exists.")

        subcategory = ProductSubcategory.objects.get(pk=subcategory_id)
        
        # Create and save the product using the provided data
        product = Product(
            prod_name=product_name,
            sub_categ_id=subcategory,
            price=price,
            stock_quantity=quantity,
            user_id=request.user
        )
        product.save()

        # Create and save the product description with images
        product_description = ProductDescription(
            prod_id=product,
            description=description,
            img1=img1,
            img2=img2,
            img3=img3,
            instructions=instruction
        )
        product_description.save()

        return redirect('product_list')  # Redirect to a product list view
    
    return render(request, 'product\save_product.html', context)


from .models import ProductSubcategory

def subcategories_view(request, categ_id):
    subcategories = ProductSubcategory.objects.filter(categ_id=categ_id)
    return render(request, 'product/subcategory_list.html', {'subcategories': subcategories})


from django.shortcuts import render
from .models import Product,ProductDescription


def subcategory_products_view(request, subcat_id):
    products = Product.objects.filter(sub_categ_id=subcat_id)
    
   
    return render(request, 'product/products.html', {'products': products})


def prod_desc(request, prod_id):
    # products = Product.objects.get(prod_id=prod_id)
    
   
    # return render(request, 'product/product_desc.html', {'products': products})
    # has_reviewed = Review.objects.filter(prod_id=prod_id, user=request.user).exists()
    product = get_object_or_404(Product, prod_id=prod_id)

    # Retrieve all reviews for the product
    reviews = Review.objects.filter(prod=product)

   

    try:
        products = Product.objects.get(prod_id=prod_id)
    except Product.DoesNotExist:
        products = None

    try:
        prod_desc = ProductDescription.objects.get(prod_id=prod_id)
    except ProductDescription.DoesNotExist:
        prod_desc = None
    
    context = {
        'products': products,
        'prod_desc': prod_desc,
        'reviews' : reviews,
    }
    
    return render(request, 'product/product_desc.html', context)

# def modify(request):
#     query = request.GET.get('q')
#     products = Product.objects.filter(user_id=request.user)

#     if query:
#         products = products.filter(Q(prod_name__icontains=query))
#     return render(request, 'product/modify_product.html', {'products': products, 'query': query})
#     # return render(request,'product/modify_product.html')

@login_required
@never_cache

def modify_product(request, prod_id):
    product = get_object_or_404(Product, prod_id=prod_id, user_id=request.user)
    description = ProductDescription.objects.get(prod_id=product)
    user_profile = UserProfile.objects.get(user=request.user)
    seller_request = SellerRequest.objects.get(user=request.user)
    user_addr = UserAddress.objects.get(user=request.user)

    if request.method == 'POST':
        product.prod_name = request.POST['prod_name']
        product.price = request.POST['price']
        product.stock_quantity=request.POST['quantity']
        product.sub_categ_id_id = request.POST['sub_categ_id']

        description.description = request.POST['description']
        description.instructions=request.POST['instruction']
        if 'img1' in request.FILES:
            description.img1 = request.FILES['img1']
        if 'img2' in request.FILES:
            description.img2 = request.FILES['img2']
        if 'img3' in request.FILES:
            description.img3 = request.FILES['img3']
        

        product.save()
        description.save()

        return redirect('product_list')

    subcategories = ProductSubcategory.objects.all()
    # try:
    #     seller_request = SellerRequest.objects.get(user=request.user)
    # except SellerRequest.DoesNotExist:
    #     seller_request = None

    # try:
    #     user_profile = UserProfile.objects.get(user=request.user)
    # except UserProfile.DoesNotExist:
    #     user_profile = None

    # try:
    #     user_addr = UserAddress.objects.get(user=request.user)
    # except UserAddress.DoesNotExist:
    #     user_addr = None
    
  
    return render(request, 'product/modify_product.html', {'product': product, 'description': description, 'subcategories': subcategories, 'user_profile': user_profile, 'seller_request': seller_request,'user_addr' : user_addr})

@login_required
@never_cache

def delete_product(request, prod_id):
    product = get_object_or_404(Product, prod_id=prod_id, user_id=request.user)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(request, 'product/delete_product.html', {'product': product})

@login_required
@never_cache

def add_cat(request):
    users = User.objects.all()
    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    
    context = {
        'users': users,
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
    }
    if request.method == 'POST':
        categ_name = request.POST['categ_name']
        categ_image = request.FILES['categ_image']

        # Create a new ProductCategory object and save it
        new_category = ProductCategory(categ_name=categ_name, categ_image=categ_image)
        new_category.save()

        return redirect('list_product_categories')  # Redirect to a list view of product categories
    else:
        return render(request, 'admin/add_cat.html',context)

from .models import ProductCategory

@login_required
@never_cache
def list_product_categories(request):
    users = User.objects.all()
    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    
    categories = ProductCategory.objects.all()
    context = {
        'users': users,
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
        'categories': categories
    }
    
    return render(request, 'admin/display_cat.html', context)

    


from django.http import JsonResponse
from django.contrib.auth.models import User

def check_username(request):
    if request.method == 'GET':
        username = request.GET.get('username', '')
        user_exists = User.objects.filter(username=username).exists()
        return JsonResponse({'exists': user_exists})

def check_email(request):
    if request.method == 'GET':
        email = request.GET.get('email', '')
        email_exists = User.objects.filter(email=email).exists()
        return JsonResponse({'exists': email_exists})


from django.shortcuts import render, redirect
from .models import AddCart, CartItems, Product
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

@login_required
@never_cache

def add_to_cart(request):
    if not request.user.is_authenticated:
        # You can implement your own logic for handling unauthenticated users
        # For example, you can redirect them to a login page
        return redirect('login_user') 

    if request.method == 'POST':
        prod_id = request.POST.get('prod_id')
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if not provided

        if prod_id:
            try:
                prod = Product.objects.get(prod_id=prod_id)
            except Product.DoesNotExist:
                return HttpResponseBadRequest("Invalid product ID")

            user = request.user
            cart, created = AddCart.objects.get_or_create(user=user)

            # Check if the product is already in the cart, if so, update the quantity
            existing_item = CartItems.objects.filter(cart=cart, prod=prod).first()
            if existing_item:
                existing_item.quantity += quantity
                existing_item.save()
            else:
                # Create a new cart item
                CartItems.objects.create(cart=cart, prod=prod, quantity=quantity)

            return redirect('cart_details')  # Redirect to the cart page or wherever you want
        else:
            return HttpResponseBadRequest("Invalid product ID")

    # Handle GET requests (e.g., rendering the page with a form)
    return render(request, 'add_to_cart.html')


# from .models import AddCart, CartItems
# from django.db.models import Sum 
# from decimal import Decimal

# def cart_details(request):
#     user = request.user
#     try:
#         cart = AddCart.objects.get(user=user)
#         cart_items = CartItems.objects.filter(cart=cart)
#         total_cart_value = cart_items.aggregate(Sum('total_price'))['total_price__sum']
#         shipping_cost = Decimal('50.00')  # Assuming a fixed shipping cost of $50.00
#         multiplied_value = total_cart_value + shipping_cost
#     except AddCart.DoesNotExist:
#         # cart = None
#         # cart_items = []
#         # total_cart_value = 0.0
#         # return redirect('index')
#         return redirect('index') 

#     return render(request, 'product/cart.html', {'cart': cart, 'cart_items': cart_items, 'total_cart_value': total_cart_value, 'multiplied_value': multiplied_value})

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Sum
from decimal import Decimal
from .models import AddCart, CartItems  # Import your models

@login_required
@never_cache

def cart_details(request):

    if request.user.is_authenticated:
        user = request.user
        try:
            cart = AddCart.objects.get(user=user)
            cart_items = CartItems.objects.filter(cart=cart)
        
        # Calculate total cart value and shipping cost
            total_cart_value = cart_items.aggregate(Sum('total_price'))['total_price__sum']
            if total_cart_value is None:
                total_cart_value = Decimal('0.00')  # Set a default value if total_cart_value is None
        
            shipping_cost = Decimal('50.00')  # Assuming a fixed shipping cost of $50.00
        
        # Calculate the total cost with shipping
            multiplied_value = total_cart_value + shipping_cost
        except AddCart.DoesNotExist:
            return redirect('index')  # Redirect to 'index' if the user has no AddCart entry

        return render(request, 'product/cart.html', {'cart': cart, 'cart_items': cart_items, 'total_cart_value': total_cart_value, 'multiplied_value': multiplied_value})
    else:

      return redirect('login_user')
   

from django.http import JsonResponse
from .models import Product

def check_product_name(request):
    if request.method == 'GET':
        product_name = request.GET.get('product_name', '')
        product_exists = Product.objects.filter(prod_name=product_name).exists()
        return JsonResponse({'exists': product_exists})


from django.contrib.auth.models import User

@login_required
@never_cache

def users_list(request):
    users = User.objects.all()
    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    
    context = {
        'users': users,
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
    }
    
    return render(request, 'admin/users_list.html', context)

@login_required
@never_cache

def seller_request(request):
    users = User.objects.all()
    seller_requests = SellerRequest.objects.all()
    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    
    context = {
        'users': users,
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
        'seller_requests' : seller_requests
    }
    return render(request, 'admin/seller_request.html', context)
    
   


# views.py

@login_required
@never_cache

def user_profile(request):
    # user_profile = UserProfile.objects.get(user=request.user)
    
    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None

    # try:
    #     product = Product.objects.filter(user_id=request.user)
    # except Product.DoesNotExist:
    #     product = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    
    context = {
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
        # 'product' :product
    }
    
    return render(request, 'user_profile.html', context)


from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

from .models import SellerRequest  # Import your SellerRequest model here

@login_required
@never_cache

def approve_seller(request, user_id):
    # Retrieve the seller request and user objects
    seller_request = get_object_or_404(SellerRequest, user__id=user_id)

    # Approve the seller by setting is_staff to True
    seller_request.user.is_staff = True
    seller_request.user.save()

    # You can perform additional actions here if needed, e.g., send notifications, update status, etc.

    # Return a JSON response indicating success
    # return JsonResponse({'message': 'Seller approved successfully'})
    return redirect('seller_request')

@login_required
@never_cache

def dis_approve_seller(request, user_id):
    # Retrieve the seller request and user objects
    seller_request = get_object_or_404(SellerRequest, user__id=user_id)

    # Approve the seller by setting is_staff to True
    seller_request.user.is_staff = False
    seller_request.user.save()

    # You can perform additional actions here if needed, e.g., send notifications, update status, etc.

    # Return a JSON response indicating success
    # return JsonResponse({'message': 'Seller approved successfully'})
    return redirect('seller_request')


from django.shortcuts import redirect, get_object_or_404
from .models import CartItems

@login_required
@never_cache

def remove_cart_item(request, cart_item_id):
    # Get the CartItems object by cart_item_id
    cart_item = get_object_or_404(CartItems, pk=cart_item_id)

    # Remove the CartItems object from the cart
    cart_item.delete()

    return redirect('cart_details')  # Redirect to your cart page or wherever you want



from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Use CSRF exemption for simplicity in this example; consider using CSRF protection in a real application.
def check_email_existence(request):
    email = request.POST.get('email', '')

    if User.objects.filter(email=email).exists():
        data = {'exists': True}
    else:
        data = {'exists': False}

    return JsonResponse(data)



from .models import Wishlist, Product

@login_required
@never_cache

def add_to_wishlist(request, prod_id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # You can implement your own logic for handling unauthenticated users
        # For example, you can redirect them to a login page
        return redirect('login_user')  # Redirect to your login URL

    # Get the product based on prod_id
    product = get_object_or_404(Product, pk=prod_id)

    # Check if the product is not already in the user's wishlist
    if not Wishlist.objects.filter(user_id=request.user, prod_id=product).exists():
        Wishlist.objects.create(user_id=request.user, prod_id=product)

    # Redirect to a success page or back to the product detail page
    return redirect('index')  # Redirect to the product detail page


from django.shortcuts import render
from .models import Wishlist

@login_required
@never_cache

def wishlist(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # You can implement your own logic for handling unauthenticated users
        # For example, you can redirect them to a login page
        return redirect('login_user')  # Redirect to your login URL

    users = User.objects.all()

    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    

    wishlist_items = Wishlist.objects.filter(user_id=request.user)

    # subcategories = ProductSubcategory.objects.all()
    context = {
        'users': users,
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
        # 'subcategories': subcategories,
        'wishlist_items': wishlist_items
    }
    # Get the user's wishlist items

    return render(request, 'product/wishlist.html', context)


@login_required
@never_cache

def remove_wish_item(request, wish_id):
    # Get the CartItems object by cart_item_id
    wish_item = get_object_or_404(Wishlist, pk=wish_id)

    # Remove the CartItems object from the cart
    wish_item.delete()

    return redirect('wishlist')

@login_required
@never_cache

def list_product_subcat(request):
    users = User.objects.all()
    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    
    subcategories = ProductSubcategory.objects.all()
    context = {
        'users': users,
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
        'subcategories': subcategories
    }
    
    return render(request, 'admin/display_subcat.html', context)


from django.shortcuts import render, redirect
from .models import ProductCategory, ProductSubcategory

@login_required
@never_cache

def add_subcategory(request):
    if request.method == 'POST':
        categ_id = request.POST.get('categ_id')
        sub_cat_name = request.POST.get('sub_cat_name')
        subcat_image = request.FILES.get('subcat_image')

        # Create a new ProductSubcategory instance and save it
        subcategory = ProductSubcategory(categ_id_id=categ_id, sub_cat_name=sub_cat_name, subcat_image=subcat_image)
        subcategory.save()
        return redirect('list_product_subcat')  # Redirect to a list view of subcategories

    categories = ProductCategory.objects.all()
    return render(request, 'admin/add_subcat.html', {'categories': categories})


from django.http import JsonResponse

def check_gstin_exists(request):
    gstin = request.GET.get('gstin')
    exists = SellerRequest.objects.filter(gstin=gstin).exists()
    response_data = {'exists': exists}
    return JsonResponse(response_data)

from django.http import JsonResponse
from .models import ProductSubcategory

def check_subcategory_exists(request):
    sub_cat_name = request.GET.get('sub_cat_name', None)

    if sub_cat_name:
        exists = ProductSubcategory.objects.filter(sub_cat_name=sub_cat_name).exists()
    else:
        exists = False

    data = {'exists': exists}
    return JsonResponse(data)


from django.http import JsonResponse

def check_category_exists(request):
    categ_name = request.GET.get('categ_name', None)

    if categ_name:
        exists = ProductCategory.objects.filter(categ_name=categ_name).exists()
    else:
        exists = False

    data = {'exists': exists}
    return JsonResponse(data)











from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from decimal import Decimal 

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def homepage(request):
    user = request.user
    user_addr = UserAddress.objects.get(user=request.user)
    currency = 'INR'
    cart = AddCart.objects.get(user=user)
    cart_items = CartItems.objects.filter(cart=cart)
    total_cart_value = cart_items.aggregate(Sum('total_price'))['total_price__sum']
    shipping_cost = Decimal('50.00')  # Assuming a fixed shipping cost of $50.00

    total_cart_value = int(total_cart_value * 100)
    shipping_cost = int(shipping_cost * 100)

    # Calculate the total amount in paisa
    amount = total_cart_value + shipping_cost


    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                      currency=currency,
                                                      payment_capture='0',
                                                      ))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['total_cart_value'] = total_cart_value  # Add the total cart value as a string
    context['shipping_cost'] = shipping_cost  # Add the shipping cost as a string
    context['user_addr'] = user_addr

    return render(request, 'index1.html', context=context)






@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                user = request.user
                cart = AddCart.objects.get(user=user)
                cart_items = CartItems.objects.filter(cart=cart)
                total_cart_value = cart_items.aggregate(Sum('total_price'))['total_price__sum']
                shipping_cost = Decimal('50.00')  # Assuming a fixed shipping cost of $50.00

                total_cart_value = int(total_cart_value * 100)
                shipping_cost = int(shipping_cost * 100)
                amount = total_cart_value + shipping_cost

                try:
                    # capture the payment
                    razorpay_client.payment.capture(payment_id, amount)

                    # render success page on successful capture of payment
                    return render(request, 'paymentsuccess.html')
                except:
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()




from .models import Review  # Import your Review model

@login_required  # Ensure the user is authenticated to access this view
@never_cache

def submit_review(request):
    if request.method == 'POST':
        prod = request.POST.get('prod_id')
        prod = Product.objects.get(prod_id=prod)
        description = request.POST.get('description')
        
        # Calculate the rating based on the number of stars selected
        rating = int(request.POST.get('rating', 0))

        # Create a new review associated with the product and the authenticated user
        Review.objects.create(
            user=request.user,
            rating=rating,
            description=description,
            prod=prod
        )
        
        # Redirect to a success page or the product detail page
        return redirect('index')



# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import Product

# def live_search(request):
#     if request.method == 'GET':
#         search_query = request.GET.get('query', '')
#         results = Product.objects.filter(prod_name__icontains=search_query)
#         product_data = [{'name': product.prod_name, 'description': product.productdescription.description, 'price': product.price, } for product in results]
#         return JsonResponse({'products': product_data})
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product

def live_search(request):
    if request.method == 'GET':
        search_query = request.GET.get('query', '')
        results = Product.objects.filter(prod_name__icontains=search_query)
        product_data = []

        for product in results:
            product_info = {
                'name': product.prod_name,
                'description': product.productdescription.description,
                'price': product.price,
                'prod_id' : product.prod_id,
                'img1_url': product.productdescription.img1.url,  # Include img1 URL
            }
            product_data.append(product_info)

        return JsonResponse({'products': product_data})
