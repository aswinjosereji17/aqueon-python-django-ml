from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    
    # react-native
    path('user_loginnn/', views.user_loginnn, name='user_loginnn'),
    path('show_userr/', views.show_userr, name='show_userr'),
    path('update_pick/<int:order_id>/', views.update_pick, name='update_pick'),
    path('update_ready_pick/<int:order_id>/', views.update_ready_pick, name='update_ready_pick'),
    path('send_otp_to_customer_m/<int:order_id>/', views.send_otp_to_customer_m, name='send_otp_to_customer_m'),
    path('verify_order_otp_m/<int:order_id>/', views.verify_order_otp_m, name='verify_order_otp_m'),
    path('loggout/', views.user_logout, name='user_logout'),
    path('login_status/', views.check_login_status, name='check_login_status'),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)