from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('',views.index, name='index'),
    path('login_user',views.login_user,name='login_user'),
    path('register/',views.register,name='register'),
    path('seller_register',views.seller_register,name='seller_register'),
    path('loggout',views.loggout,name='loggout'),
    path('user_profile_view', views.user_profile_view, name='user_profile_view'),
    
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    # path('add_product/', views.add_product, name='add_product'), 
    # path('get_subcategories/<int:category_id>/', views.get_subcategories, name='get_subcategories'),

    path('product_list', views.product_list, name='product_list'),
    path('add_product', views.add_product, name='add_product'),
    path('subcategories/<int:categ_id>/', views.subcategories_view, name='subcategories'),
    path('subcategory_products/<int:subcat_id>/', views.subcategory_products_view, name='subcategory_products'),
    path('prod_desc/<int:prod_id>/', views.prod_desc, name='prod_desc'),
    path('modify-product/<int:prod_id>/', views.modify_product, name='modify_product'),
    path('delete-product/<int:prod_id>/', views.delete_product, name='delete_product'),

    # path('modify-product', views.modify_product, name='modify_product'),
    path('add_cat', views.add_cat, name='add_cat'),
    path('product_categories/', views.list_product_categories, name='list_product_categories'),
   
    path('check_username/', views.check_username, name='check_username'),
    path('check_email/', views.check_email, name='check_email'),

   path('edit_profile/', views.edit_profile, name='edit_profile'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
 