from django.urls import path
from .views import *
from . import views



app_name = "seller"
urlpatterns = [
     path("", views.SellerLogin, name="sellerlogin"),
     path("sellerregistration/",views.sellerregistration, name="sellerregistration"),
     path("sellerlogout/",SellerLogoutView.as_view(),name="sellerlogout"),
     path("selleraddproduct/<str:usr>/",SellerAddproduct.as_view(), name = "selleraddproduct"),
     path("sellerhome/<str:selleruser>/", SellerHome.as_view(),name="sellerhome"),
     path("<str:st>-<int:pk>/",SellerOrderDetailView.as_view(), name="sellerorderdetail"),
     path("<str:store_name>/",SellerProfile.as_view(), name="sellerprofile"),
     
     
]
