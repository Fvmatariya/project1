from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('OTP/',views.otp,name='OTP'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('forgot-password2/',views.forgot_password2,name='forgot-password2'),
    path('forgot-password3/',views.forgot_password3,name='forgot-password3'),
    path('add-product/',views.add_product,name='add-product'), 
    path('all-product/',views.all_product,name='all-product'), 
    path('delete-product/<int:pk>',views.delete_product,name='delete-product'),
    path('edit-product/<int:pk>',views.edit_product,name='edit-product'),
    path('product_details/<int:pk>',views.product_details,name='product_details'),
    path('add-to-cart/<int:pk>',views.add_to_cart,name='add-to-cart'),
    path('delete-from-cart/<int:pk>',views.delete_cart,name='delete-from-cart'),
    path('about/',views.about,name='about'),
    path('blog-details/',views.blog_details,name='blog-details'),
    path('blog/',views.blog,name='blog'),
    path('cart/',views.cart,name='cart'),
    path('order/',views.order,name='order'),
    path('checkout/',views.checkout,name='checkout'),
    path('buy-product/<int:pk>',views.buy_product,name='buy-product'),
    path('buy-product/paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('delete_order/<int:pk>',views.delete_order,name='delete_order'),
    path('delivered/<int:pk>',views.delivered,name='delivered'),
    path('contact/',views.contact,name='contact'),
    path('elements',views.elements,name='elements'),
    path('login/',views.login,name='login'),
    path('confirmation/',views.confirmation,name='confirmation'),
    path('register/',views.register,name='register'),
    path('shop/',views.shop,name='shop'),

]