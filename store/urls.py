from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    re_path(r'viewItem/(?P<product_id>\d+)/$', views.viewItem, name="viewItem"),
]