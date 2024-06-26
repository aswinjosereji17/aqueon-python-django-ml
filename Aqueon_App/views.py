from django.shortcuts import render

# Create your views here.


# react
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.cache import never_cache

@csrf_exempt 
@never_cache
def user_loginnn(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def check_login_status(request):
    """
    View to check if the user is logged in.
    """
    # If the user is authenticated, return logged in status as true
    if request.user.is_authenticated:
        return JsonResponse({'loggedIn': True})
    else:
        return JsonResponse({'loggedIn': False})


@never_cache
@csrf_exempt 
# @require_GET
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})

from Website.models import ProductCategory,AssignedDeliveryAgent,Order,OrderItem,OrderNotification_Seller,UserProfile
# def show_user(request):
#     # Retrieve all user profiles from the database
#     user_profiles = ProductCategory.objects.all()
    
#     # Convert user profiles to JSON format
#     user_profiles_json = [
#         {
#             'id': profile.categ_id,
#             'name': profile.categ_name,
#             'image': request.build_absolute_uri(profile.categ_image.url) if profile.categ_image else None,
#             'craeted_at': profile.created_at,

#         }
#         for profile in user_profiles
#     ]
    
#     # Return the user profiles as a JSON response
#     return JsonResponse(user_profiles_json, safe=False)


@never_cache
def show_userr(request):
    del_req = AssignedDeliveryAgent.objects.filter(deliveryagent=request.user).order_by('-created_at')
    del_req_json=[
        {'order_id':d_r.id,
         'serial_no': d_r.order.serial_number,
         'status': d_r.status,
         'ready_for_pickup' :d_r.ready_for_pickup,
         'delivered' : d_r.delivered,
         
         } for d_r in del_req
    ]
    return JsonResponse(del_req_json, safe=False)


# from django.shortcuts import redirect
# from django.http import JsonResponse

# def update_picked(request, order_id):
#     notification = AssignedDeliveryAgent.objects.get(pk=order_id)
    
#     if request.method == 'POST':
#         # Perform the update
#         notification.status = 'PI' 
#         notification.save()
#         return JsonResponse({'message': 'Successfully updated status'}, status=200) 

#     return JsonResponse({'message': 'Invalid request method'}, status=405)

from django.http import JsonResponse

from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt

@never_cache
@csrf_exempt
def update_pick(request, order_id):
    if request.method == 'POST':
        try:
            notification = AssignedDeliveryAgent.objects.get(pk=order_id)
            notification.status = 'PI'
            notification.save()
            return JsonResponse({'message': 'Status updated successfully'})
        except AssignedDeliveryAgent.DoesNotExist:
            return JsonResponse({'error': 'Notification not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@never_cache
@csrf_exempt
def update_ready_pick(request, order_id):
    if request.method == 'POST':
        try:
            notification = AssignedDeliveryAgent.objects.get(pk=order_id)
            notification.ready_for_pickup = True
            notification.save()
            return JsonResponse({'message': 'Ready for pickup-django'})
        except AssignedDeliveryAgent.DoesNotExist:
            return JsonResponse({'error': 'django-ready for pickup'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


from twilio.rest import Client

@never_cache
def send_otp_via_sms_m(mobile_number, otp):
    # Your Twilio credentials
    account_sid = 'AC86b9d0d8ebd858f6ea5b7cda55f04710'
    auth_token = '1c4df17e85d7334d4e5fb7dc675efeb7'
    twilio_number = '+13237452215'
    
    # Initialize Twilio client
    client = Client(account_sid, auth_token)
    v_mobile_number = '+91' + mobile_number
    print(v_mobile_number)
    
    # Compose the message
    message_body = f"Your OTP for verification is: {otp}"
    
    # Send the SMS
    client.messages.create(from_=twilio_number, body=message_body, to=v_mobile_number)


import random
@never_cache
@csrf_exempt
def send_otp_to_customer_m(request, order_id):
    if request.method == 'POST':
        try:
            order = AssignedDeliveryAgent.objects.get(pk=order_id)
            user = Order.objects.get(pk=order.order.id)
            user_profile = UserProfile.objects.get(user=user.user)
            
            # Generate OTP
            otp = ''.join(random.choices('0123456789', k=6))
            order.otp = otp
            order.save()
            
            # Send OTP via SMS
            send_otp_via_sms_m(user_profile.mobile, otp)
            
            return JsonResponse({'message': 'OTP sent successfully'})
        except (AssignedDeliveryAgent.DoesNotExist, Order.DoesNotExist, UserProfile.DoesNotExist) as e:
            return JsonResponse({'error': 'Order or user profile not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        # return redirect('del_reqs')
    

from django.http import JsonResponse
@never_cache
@csrf_exempt
def verify_order_otp_m(request, order_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            otp_entered = data.get('otpInput')
            # otp_entered = request.POST.get('otp')
            
            # Retrieve the order object
            order = AssignedDeliveryAgent.objects.get(pk=order_id)
            o_t=order.otp
            print(otp_entered)
            print(o_t)
            
            # Check if the entered OTP matches the OTP stored in the order and it's not null
            if order.otp == otp_entered and order.otp != 'Null':
                # Update the order to mark it as verified
                order.otp = '0'  # Assuming OTP is stored as a string
                order.delivered = True
                order.save()
                
                # Return a success response
                return JsonResponse({'message': 'OTP verified successfully'}, status=200)
            else:
                # Return an error response if the OTP is incorrect or null
                return JsonResponse({'error': 'Invalid OTP. Please try again.'}, status=400)
        except AssignedDeliveryAgent.DoesNotExist:
            return JsonResponse({'error': 'AssignedDeliveryAgent not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)