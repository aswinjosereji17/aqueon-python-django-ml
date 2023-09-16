from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import UserProfile, Product, SellerRequest, HomeSpecialOffer, ProductCategory,UserAddress
from django.contrib.auth.decorators import login_required
from django.db.models import Q



# Create your views here.
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
            cart_item_count = cart_items.count()  # Calculate the count of items in the cart
        except AddCart.DoesNotExist:
            cart = None
            cart_items = []
            cart_item_count = 0
        context = {
        'cart' : cart,
        'cart_items' : cart_items,
        'homeimg': homeimg,
        'prod_cat':prod_cat,
        'cart_item_count': cart_item_count,
        'recent_products': recent_products
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
def loggout(request):
    # print('Logged Out')
    logout(request)
    return redirect('index')


from django.shortcuts import render
from .models import UserProfile,Product, ProductSubcategory, UserAddress

# def user_profile_view(request):
#     user_profile = UserProfile.objects.get(user=request.user)
    
#     context = {
#         'user_profile': user_profile,
#     }
#     return render(request, 'user_profile.html', context)
@login_required
def user_profile_view(request):
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
    
    return render(request, 'user_prof.html', context)


from django.shortcuts import render, redirect
from .models import UserProfile, UserAddress,SellerRequest
from django.contrib.auth.decorators import login_required


# 4-09-2023
@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Get the current user's profile
        user_profile = UserProfile.objects.get(user=request.user)
        user = User.objects.get(username=request.user)
        user_addr= UserAddress.objects.get(user=request.user)

        # Update the profile fields with the submitted form data
        user_profile.mobile = request.POST.get('mobile')
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
    }
    
    return render(request, 'product/product_desc.html', context)

# def modify(request):
#     query = request.GET.get('q')
#     products = Product.objects.filter(user_id=request.user)

#     if query:
#         products = products.filter(Q(prod_name__icontains=query))
#     return render(request, 'product/modify_product.html', {'products': products, 'query': query})
#     # return render(request,'product/modify_product.html')

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

def delete_product(request, prod_id):
    product = get_object_or_404(Product, prod_id=prod_id, user_id=request.user)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(request, 'product/delete_product.html', {'product': product})


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

        return redirect('user_profile_view')  # Redirect to a list view of product categories
    else:
        return render(request, 'admin/add_cat.html',context)

from .models import ProductCategory

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
def add_to_cart(request):
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
from django.http import JsonResponse

def check_category_exists(request):
    if request.method == 'POST':
        categ_name = request.POST.get('categ_name')
        if ProductCategory.objects.filter(categ_name=categ_name).exists():
            return JsonResponse({'message': 'Category already exists'}, status=400)
        else:
            return JsonResponse({'message': 'Category does not exist'})



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