from django.urls import path
from .views import *


app_name = "deals"
urlpatterns = [
    
     path("" , HomeView.as_view() , name="home"),
     path("about/", AboutView.as_view(), name="about"),
     path("all_products/", All_ProductsView.as_view(), name="all_product"),
     path("product/<str:slug>/" ,ProductDetailView.as_view(),name = "productdetail"),
     path("add-to-cart-<int:pro_id>/" , AddtoCartView.as_view(), name="addtocart"),
     path("my-cart/", MyCartView.as_view(), name="mycart"),
     path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
     path("empty-cart/", EmptyCartView.as_view(), name="emptycart"),
     path("checkout/", CheckoutView.as_view(), name="checkout"),
     path("register/", CustomerRegistrationView.as_view(), name="customerregistration"),
     path("logout/",CustomerLogoutView.as_view(), name="customerlogout"),
     path("login/",CustomerLoginView.as_view(), name="customerlogin"),
     path("profile/",CustomerprofileView.as_view(), name="customerprofile"),
     path("profile/order-<int:pk>/",CustomerOrderDetailView.as_view(), name="customerorderdetail"),



     path("<str:name>/" , Category_view.as_view(), name = "category"),
    

]
