from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import UserProfile, SellerRequest, HomeSpecialOffer, ProductCategory,UserAddress
from django.contrib.auth.decorators import login_required
from django.db.models import Q



# Create your views here.
def index(request):
    homeimg = HomeSpecialOffer.objects.all()  # Get all events from the database
    prod_cat = ProductCategory.objects.all()  # Get all events from the database

    context = {
        'homeimg': homeimg,
        'prod_cat':prod_cat
    }
    # return render(request, 'showsevents.html', context)
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
            UserProfile.objects.create(user=user, mobile="")
            UserAddress.objects.create(user=user,address1="",address2="")
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
            UserProfile.objects.create(user=user, mobile="")
            UserAddress.objects.create(user=user,address1="",address2="")  
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
        user_profile.save()

        user_addr.address1=request.POST.get('address1')
        user_addr.address2=request.POST.get('address2')
        user_addr.save()

        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        user.email=request.POST.get('email')
        user.save()

        # seller_req.company=request.POST.get('company')
        # seller_req.save()
        if request.user.is_staff and not request.user.is_superuser :
            # Get or create a SellerRequest object
            seller_req=SellerRequest.objects.get(user=request.user)
            seller_req.company = request.POST.get('company')
            seller_req.save()  

        
        # Redirect to a success page or profile page
        return redirect('user_profile_view')

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

    if query:
        products = products.filter(Q(prod_name__icontains=query))

    return render(request, 'product\product_list.html', {'products': products, 'query': query})




@login_required
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        subcategory_id = request.POST['subcategory']
        price = request.POST['price']
        description = request.POST['description']
        instruction = request.POST['instruction']
        img1 = request.FILES['img1']
        img2 = request.FILES['img2']
        img3 = request.FILES['img3']

        subcategory = ProductSubcategory.objects.get(pk=subcategory_id)
        
        # Create and save the product using the provided data
        product = Product(
            prod_name=product_name,
            sub_categ_id=subcategory,
            price=price,
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
    
    subcategories = ProductSubcategory.objects.all()
    return render(request, 'product\save_product.html', {'subcategories': subcategories})


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

    if request.method == 'POST':
        product.prod_name = request.POST['prod_name']
        product.price = request.POST['price']
        product.sub_categ_id_id = request.POST['sub_categ_id']

        description.description = request.POST['description']
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
    return render(request, 'product/modify_product.html', {'product': product, 'description': description, 'subcategories': subcategories})

