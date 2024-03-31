# context_processors.py

from Website.models import AddCart, CartItems, Wishlist,Subscription

from django.utils import timezone

def user_data(request):
    data = {}
    
    if request.user.is_authenticated:
        user = request.user
        
        try:
            cart = AddCart.objects.get(user=user)
            cart_items = CartItems.objects.filter(cart=cart)
            cart_item_count = cart_items.count()
            user_id = request.user.id
            wish_count = Wishlist.objects.filter(user_id=user_id).count()
            subscriptions = Subscription.objects.filter(user=user)
            for subscription in subscriptions:
                if subscription.expiration_date and subscription.expiration_date < timezone.now().date():
                    subscription.status = False
                    subscription.save()

        except AddCart.DoesNotExist:
            cart = None
            cart_items = []
            cart_item_count = 0
            wish_count = 0
    else:
        cart = None
        cart_items = []
        cart_item_count = 0
        wish_count = 0

    data['cart'] = cart
    data['cart_items'] = cart_items
    data['cart_item_count'] = cart_item_count
    data['wish_count'] = wish_count

    return data


