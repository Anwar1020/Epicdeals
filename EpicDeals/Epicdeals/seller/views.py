from typing import Any, Dict
from django import http
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View, CreateView,FormView,DetailView
from deals.models import *
from django.urls import resolve
from deals.forms import CheckoutForm,CustomerRegistrationForm,CustomerloginForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .import urls
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404
# Create your views here.


def SellerLogin(request):
    if request.method == 'POST':
        s_name = request.POST['store_name']
        pword = request.POST['password']
        seller_user = authenticate(username = s_name, password = pword)

        if seller_user is not None and Seller_store.objects.filter(store_name = s_name).exists():
            login(request,seller_user)
            redirect_url = reverse("seller:sellerprofile", args=[s_name])
            return redirect(redirect_url)
            
        else:
            messages.info(request, "Invalid store name and password")
            return redirect('seller:sellerlogin')
        

       
        
    else:
        return render(request, 'sellerlogin.html')
    

    


def sellerregistration(request,self):
    if request.method == "POST":
        store_name = request.POST['store_name']
        bank_account = 2535
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        contact_number = request.POST['contact_number']
        
        if Seller_store.objects.filter(store_name = store_name).exists():
            messages.info(request,"Store name is already exist, try with another store_name")
            return redirect('seller:sellerregistration')
        else:
            seller_user = User.objects.create_user(store_name, email, password)
            seller_store_obj = Seller_store.objects.create(seller_user = seller_user,password = password, store_name = store_name,
                                                       bank_account = bank_account,address=address,contact_number = contact_number,email=email)
            seller_store_obj.save()
            return redirect('seller:sellerlogin')
        
    else:
        return render(self.request, "sellerregistration.html")



class SellerLogoutView(View):

    def get(self, request):
        logout(request)
        return redirect("seller:sellerlogin")
    
     

class SellerProfile(TemplateView):
    template_name = "sellerprofile.html"
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        seller_store = self.kwargs["store_name"]
        context["product_details"] = Product.objects.filter(
                  cartproduct__cart__order__order_status='Order Received',
                  cartproduct__cart__order__cart__cartproduct__product__seller_store__store_name=seller_store)

        context["seller_store"] = seller_store
        context["pendingorders"] = Order.objects.filter( cart__cartproduct__product__seller_store__store_name = seller_store , order_status = "Order Received")
        
        context["seller_info"] = self.request.user.seller_store
        
        
        return context
    

class SellerOrderDetailView(TemplateView):
    template_name = "sellerorder.html"
   
    def get_context_data(self,**kwargs):
        context =  super().get_context_data(**kwargs)
        ord_id = self.kwargs["pk"]
        st = self.kwargs['st']
        context["st"] = st
        ord_obj = Order.objects.filter(id = ord_id)
        print(ord_obj)
        context["order_obj"] = ord_obj
        return context
    

    def post(self, request, *args, **kwargs):
        ord_id = self.kwargs["pk"]
        payment_status = request.POST.get("payment_status")
        ord_obj = Order.objects.get(id=ord_id)
        ord_obj.payment_status = payment_status
        ord_obj.save()
        return redirect("seller:sellerorderdetail", st=self.kwargs["st"], pk=ord_id)



class SellerAddproduct(TemplateView):
    template_name = "selleraddproduct.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["st"] = self.kwargs["usr"]
        return context

    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        slug = request.POST.get("slug")
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)
        image = request.FILES.get("image")
        marked_price = request.POST.get("marked_price")
        selling_price = request.POST.get("selling_price")
        description = request.POST.get("description")
        warranty = request.POST.get("warranty")
        return_policy = request.POST.get("return_policy")
        
        # Assign the current user as the seller_store
        st = self.kwargs["usr"]
        seller_store = Seller_store.objects.get(store_name = st)
        print(request.user.seller_store)

        product = Product.objects.create(
            title=title,
            slug=slug,
            category=category,
            image=image,
            marked_price=marked_price,
            selling_price=selling_price,
            description=description,
            warranty=warranty,
            return_policy=return_policy,
            seller_store=seller_store,
        )
        product.save()

        return redirect("seller:sellerhome", seller_store)




class SellerHome(TemplateView):
    template_name="sellerhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        st = self.kwargs["selleruser"]
        seller_store = Seller_store.objects.get(store_name = st)
        context["products"] = Product.objects.filter(seller_store = seller_store)
        context["orders"] = Order.objects.filter(cart__cartproduct__product__seller_store__store_name = st)
        return context