from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views
cream = "crop"
urlpatterns = [
    re_path(r'^$',views.homepage, name='home'),

    re_path(r'^createshop$',views.createShop, name='createshop'),
    re_path(r'^cart$',views.cart, name='cart'),
    re_path(r'^item/(?P<itemname>[\w ]+)/$',views.item,name = 'item'),

    re_path(r'^art$',views.art),
    re_path(r'^manage$',views.manage, name='manage'),
    re_path(r'^makemanager$',views.makemanager),
    re_path(r'^searchItems$',views.searchItems),
    re_path(r'^login$',views.login,name = 'login'),
    re_path(r'^register$',views.register,name = 'register'),
    re_path(r'^shop$',views.shops,name = 'shop'),
    re_path(r'^shops$',views.shops, name = "shops"),
    re_path(r'^shop/(?P<shopname>[\w ]+)/$',views.shop),
    re_path(r'^exit$',views.exit, name='exit'),
    re_path(r'^manageItemsShop',views.manage, name='manageItemsShop'),
    re_path(r'^manageItemsShop/(?P<shopname>[\w ]+)/$',views.shop),

    
    re_path(r'ws/socket-server/',views.ChatConsumer.as_asgi()),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)