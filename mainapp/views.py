from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from mainapp import constants
from mainapp.models import Sale,Category
from mainapp.forms import SalePaymentForm
from mainapp.models import Tag,ItemTag,Item,Sub_Cat

from pusher import Pusher

from allauth.account.signals import user_logged_in
from allauth.account.signals import user_signed_up


class RemoveItem(View):

    def get(self,request):
        name=request.GET['id']
        if name in request.session['cart']:
            del request.session['cart'][name]
            request.session['cart'] = request.session['cart']
        else:
            return HttpResponse("Failed!")
        return HttpResponse("a:b")

removeitem = login_required(RemoveItem.as_view())

class AllProduct(View):

    def get(self,request):
        id = request.GET['id']
        get_product_id = Category.objects.get(name=id)
        get_product_id = get_product_id.id
        cat_obj = Sub_Cat.objects.filter(p_id=get_product_id)
        photo,name = [],[]
        for x in cat_obj:
            name.append(x.name)
            photo.append("shopping_cart/"+x.image.name)
        photo = iter(photo)
        context = {'ref':name,"to_ref":True,'t':id,"photo":photo}
        return render(request, 'mainapp/first.html', context)
allproduct = login_required(AllProduct.as_view())

class MainPage(View):

    def get(self,request):
        cat_obj = Category.objects.all()
        photo = []
        name = []
        for x in cat_obj:
            name.append(x.name)
            photo.append("shopping_cart/"+x.photo.name)
        photo = iter(photo)
        context = {'ref':name,"to_ref":False,'t':"MainCategories","photo":photo}
        return render(request, 'mainapp/first.html', context)
mainpage = login_required(MainPage.as_view())
       
class CategoryList(View):

    def get(self,request):
        id = request.GET['id']
        context = {'ref':cat,"to_ref":True,'t':id}
        return render(request, "mainapp/first.html", context)

categorylist = login_required(CategoryList.as_view())

class Logic(View):

    def get(self,request):
            tag = request.GET['id']
            tag=tag.split(" ")
            print tag
            itemlist,pricelist,photo = [],[],[]
            for t in tag:
                d = Tag.objects.filter(tag_title__icontains=t)
                for i in d:
                    itemtagobj = ItemTag.objects.filter(tag_id=i.id)
                    for x in itemtagobj:
                        itemobj = Item.objects.get(id = x.item_id.id)
                        itemlist.append(itemobj.item_name)
                        pricelist.append(itemobj.price)
                        photo.append("shopping_cart/"+itemobj.photo.name)
            price = iter(pricelist)
            photo = iter(photo)
            context = {'ref':itemlist,"to_ref":False,"p":price,'photo':photo}
            return render(request, "mainapp/itemlist.html", context)

logic = login_required(Logic.as_view())

class Cart(View):

    def get(self,request):
        itemname = request.GET['id']

cart = login_required(Cart.as_view())

class ViewCart(View):

    def get(self,request):
        cart = request.session.get('cart', {})
        price,image = [],[]
        total = 0.0
        for item in cart:
            a = Item.objects.get(item_name__exact=item)
            image.append('shopping_cart/'+a.photo.name)
            price.append(a.price)
            total += a.price
        price = iter(price)
        image = iter(image)
        context = {'cart':cart,'price':price,'total':total,'image':image}
        return render(request, "mainapp/cart.html", context)

viewcart = login_required(ViewCart.as_view())

class AddCart(View):
    
    def get(self,request):
        item_name = request.GET['id']
        # item_name = str(item_name)
        cart = request.session.get('cart', {})
        cart[item_name] = item_name
        request.session['cart'] = cart
        return HttpResponse("Added Sucessfully!")

addcart = login_required(AddCart.as_view())

def charge(request):
    if request.method == "POST":
        form = SalePaymentForm(request.POST)
        form.amount = request.GET['id']
        if form.is_valid(): # charges the card
            return redirect("/accounts/login/")
    else:
        form = SalePaymentForm()
        form.amount =request.GET['id']
 
    return render(request,"mainapp/charge.html",{'form': form})