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
    path('list_product_subcat/', views.list_product_subcat, name='list_product_subcat'),
    path('add_subcategory/', views.add_subcategory, name='add_subcategory'),

    path('check_username/', views.check_username, name='check_username'),
    path('check_email/', views.check_email, name='check_email'),




    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart_details', views.cart_details, name='cart_details'),
    path('check_product_name/', views.check_product_name, name='check_product_name'),

    path('users_list/', views.users_list, name='users_list'),
    path('seller_request/', views.seller_request, name='seller_request'),

    path('check-category-exists/', views.check_category_exists, name='check-category-exists'),    path('user_profile/', views.user_profile, name='user_profile'),
    path('approve-seller/<int:user_id>/', views.approve_seller, name='approve_seller'),
    path('dis_approve-seller/<int:user_id>/', views.dis_approve_seller, name='dis_approve_seller'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('add_to_wishlist/<int:prod_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    path('check_gstin_exists/', views.check_gstin_exists, name='check-gstin-exists'),
    path('check-subcategory-exists/', views.check_subcategory_exists, name='check-subcategory-exists'),
    path('remove_wish_item/<int:wish_id>/', views.remove_wish_item, name='remove_wish_item'),



    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
 