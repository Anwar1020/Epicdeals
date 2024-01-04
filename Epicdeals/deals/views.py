from typing import Any, Dict
from django import http
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View, CreateView,FormView,DetailView
from .models import *
from django.urls import resolve
from .forms import CheckoutForm,CustomerRegistrationForm,CustomerloginForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
# Create your views here.


class Ecommixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id = cart_id)
            if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
                cart_obj.customer = request.user.customer
                cart_obj.save()
            
        return super().dispatch(request,*args,kwargs)


        



class HomeView(Ecommixin, TemplateView ):
    template_name = "home.html"
    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)
        context['category'] = Category.objects.all()
        context['product_list'] = Product.objects.all()
        return context





class All_ProductsView(Ecommixin, TemplateView):
    template_name = "all_products.html"
    
    def get_context_data(self,**kwarg,):
        context = super().get_context_data(**kwarg)
        context['category'] = Category.objects.all()
        return context 






class Category_view(Ecommixin, TemplateView):
    template_name = "catagory.html"
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        name = self.kwargs['name']
        context['category'] = Category.objects.all()

        products = Product.objects.all().filter(category__slug=name)
        context['product_list'] = products
        return context 



class ProductDetailView(Ecommixin, TemplateView):
    template_name = "productdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        url_slug = self.kwargs["slug"]
        product = Product.objects.get(slug = url_slug)
        context['category'] = Category.objects.all()
        context["product"] = product
        
        return context


class AddtoCartView(Ecommixin, TemplateView):
    template_name = "addtocart.html"
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        #get product id from url req
        product_id = self.kwargs['pro_id']
        #get product
        product_obj = Product.objects.get(id=product_id) 

        #if cart exist in out database
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product = product_obj)
            #if item is already exist()
            if this_product_in_cart.exists():
                cartprodcut = this_product_in_cart.last()
                cartprodcut.quantity += 1
                cartprodcut.subtotal += product_obj.selling_price
                cartprodcut.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()

            else:
                cartprodcut = CartProduct.objects.create(cart = cart_obj, product = product_obj, 
                                                         rate = product_obj.selling_price, quantity = 1,subtotal = product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()


        else:
            print("dksfjksdf")
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartprodcut = CartProduct.objects.create(cart = cart_obj, product = product_obj, 
                                                         rate = product_obj.selling_price, quantity = 1,subtotal = product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
            



        return context

class MyCartView(Ecommixin, TemplateView):
    template_name = "mycart.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context




class ManageCartView(Ecommixin,View):
    def get(self, request, *arg, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        if action=="inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action=="dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity==0:
                cp_obj.delete()
            
        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()

            
        else:
            pass


        return redirect("deals:mycart") 



class EmptyCartView(Ecommixin,View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id",None) 
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()

        return redirect("deals:mycart")





class CheckoutView(Ecommixin, CreateView):
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("deals:about")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj


        return context
    def form_valid(self, form): 
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']
        else:
            return redirect("deals:home")
        return super().form_valid(form)
    





         
class CustomerRegistrationView(CreateView):
    template_name = "customerregistration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy('deals:home')

    def form_valid(self,form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)


        return super().form_valid(form)
    
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("deals:home")
    



class CustomerLoginView(FormView):
    template_name = "customerlogin.html"
    form_class = CustomerloginForm
    success_url = reverse_lazy('deals:home')

    #form valid method is a type of post method
    def form_valid(self,form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password = pword)
        print(usr)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            print(uname + pword)
            return render(self.request,self.template_name,{"form":self.form_class, "error":"invalid login"})
        
        return super().form_valid(form)
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url
      




class CustomerprofileView(TemplateView):
    template_name = "customerprofile.html"
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self,**kwarg,):
        context = super().get_context_data(**kwarg)
        customer = self.request.user.customer
        context['customer']=customer
        orders = Order.objects.filter(cart__customer=customer).order_by("-id")
        context["orders"] = orders
        return context
         

class CustomerOrderDetailView(DetailView):
    template_name = "customerorderdetail.html"
    model = Order
    context_object_name = "ord_obj"
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?/profile/")
        return super().dispatch(request, *args, **kwargs)




class AboutView (TemplateView):
    template_name = "about.html"
    def get_context_data(self,**kwarg,):
        context = super().get_context_data(**kwarg)
        context['category'] = Category.objects.all()
        return context 
def sun():
    a = 5
    b = 20
    return a+b








