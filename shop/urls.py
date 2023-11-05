from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ path('',views.store_view,name="store" ),
                path('cart/',views.cart_view,name="cart" ),
                path('product/',views.product_view ),
                path('update-item/',views.update_cart ),
                path('checkout/',views.checkout_view ),                
                path('admin/', admin.site.urls),]
