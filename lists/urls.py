from django.urls import path, include
from . import views



urlpatterns = [
    #######
    #  Base
    path("lists/", views.lists, name="lists"),

    ########
    #  Lists
    path("lists/list_info/<str:primary_key_list>/", views.list_info, name="list_info"),
    path("lists/delete_list/<str:primary_key_list>", views.delete_list, name="delete_list"),

    ###########
    #  Products
    path("lists/products/", views.products, name="products"),
    path("lists/products/product_data/<str:primary_key_product>", views.product_data, name='product_data'),
    path("lists/products/edit_products", views.edit_products, name="edit_products"),
    path("lists/products/edit_product/<str:primary_key_product>", views.edit_product, name='edit_product'),
    path("lists/list_info/<str:primary_key_list>/delete_product_w_price/<str:primary_key_product_w_price>", views.delete_product_w_price, name='delete_product_w_price'),
    path("lists/delete_product/<str:primary_key_product>", views.delete_product, name='delete_product'),
    
    #########
    #  Stores
    path("lists/products/edit_stores", views.edit_stores, name="edit_stores"),
    path("lists/products/edit_stores/edit_store/<str:primary_key_store>", views.edit_store, name="edit_store"),
    path("lists/products/edit_stores/delete_store/<str:primary_key_store>", views.delete_store, name="delete_store"),
    
    ########
    #  Units
    path("lists/products/edit_units", views.edit_units, name="edit_units"),
    path("lists/products/edit_units/edit_unit/<str:primary_key_unit>", views.edit_unit, name="edit_unit"),
    path("lists/products/edit_units/delete_unit/<str:primary_key_unit>", views.delete_unit, name="delete_unit"),
    
    #######
    #  Test
    path("lists/tests", views.create_test, name="create_test"),
]
