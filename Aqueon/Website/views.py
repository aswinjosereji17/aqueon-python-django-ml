from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import UserProfile, SellerRequest, HomeSpecialOffer
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    homeimg = HomeSpecialOffer.objects.all()  # Get all events from the database
    context = {
        'homeimg': homeimg,  # Pass the events to the template context
    }
    # return render(request, 'showsevents.html', context)
    return render(request,'index.html', context)

def login_user(request):
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
            UserProfile.objects.create(user=user, address="")
            success_message = "Registration successful. You can now log in."
            messages.success(request, success_message)
            return redirect('login_user')
           
    else:
        return render (request, "register.html")

def seller_register(request):
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
            gstin = request.POST['gstin']
            document = request.FILES.get('document')
            seller_request = SellerRequest.objects.create(user=user, gstin=gstin, document=document)
            user.save()
            success_message = "Seller request submitted. Please wait for approval."
            UserProfile.objects.create(user=user, address="")
            return redirect('login_user')
           
    else:
        return render(request, "seller_reg.html")

def loggout(request):
    # print('Logged Out')
    logout(request)
    return redirect('index')


from django.shortcuts import render
from .models import UserProfile

@login_required
# def user_profile_view(request):
#     user_profile = UserProfile.objects.get(user=request.user)
    
#     context = {
#         'user_profile': user_profile,
#     }
#     return render(request, 'user_profile.html', context)

def user_profile_view(request):
    # user_profile = UserProfile.objects.get(user=request.user)
    
    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    context = {
        'user_profile': user_profile,
        'seller_request': seller_request,
    }
    
    return render(request, 'user_profile.html', context)


