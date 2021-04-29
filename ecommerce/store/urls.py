from django.urls import path
from . import views
app_name = "store"
urlpatterns = [
    path('cart/',views.cart,name = "cart"),
    path('checkOut/',views.checkOut,name = "checkOut"),
    path('',views.store,name="store"),
    path('emptycart/',views.emptycart,name="emptycart"),
    path('user_register/',views.user_register,name="user_register"),
    path('user_login/',views.user_login,name="user_login"),
    path('invalid_login/',views.invalid_login,name="invalid_login"),
]
