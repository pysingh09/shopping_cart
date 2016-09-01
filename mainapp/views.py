from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from mainapp import constants
from mainapp.models import Sale,Category
from mainapp.forms import SalePaymentForm
from mainapp.models import Tag,ItemTag,Item,Sub_Cat

from pusher import Pusher

from allauth.account.signals import user_logged_in
from allauth.account.signals import user_signed_up

class Delete_From_Cart(View):
    def get(self,request):
        name=request.GET['id']
        print request.session['cart']
        if name in request.session['cart']:
            del request.session['cart'][name]
            request.session['cart']=request.session['cart']
        else:
            return HttpResponse("Failed!")
        return HttpResponse("Sucessfully Deleted From Cart !")

class ProductAll(View):
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

class FirstScreen(View):
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
       

class CategoryList(View):
    def get(self,request):
        id = request.GET['id']
        context = {'ref':cat,"to_ref":True,'t':id}
        return render(request, "mainapp/first.html", context)

class Logic(View):
    def get(self,request):
            tag = request.GET['id']
            d = Tag.objects.get(tag_title__exact=tag)
            itemtagobj = ItemTag.objects.filter(tag_id=d.tag_id)
            itemlist,pricelist,photo = [],[],[]
            for x in itemtagobj:
                d = Item.objects.get(id = x.item_id.id)
                itemlist.append(d.item_name)
                pricelist.append(d.price)
                photo.append("shopping_cart/"+d.photo.name)
            price = iter(pricelist)
            photo = iter(photo)
            context = {'ref':itemlist,"to_ref":False,"p":price,'photo':photo}
            return render(request, "mainapp/itemlist.html", context)


class Cart(View):
    def get(self,request):
        itemname = request.GET['id']

class View_cart(View):
    def get(self,request):
        cart = request.session.get('cart', {})
        price,image = [],[]
        total = 0.0
        for item in cart:
            item = item.replace("_"," ")
            a = Item.objects.get(item_name__exact=item)
            image.append('shopping_cart/'+a.photo.name)
            price.append(a.price)
            total += a.price
        price = iter(price)
        image = iter(image)
        context = {'cart':cart,'price':price,'total':total,'image':image}
        return render(request, "mainapp/cart.html", context)

class Add_to_cart(View):
    def get(self,request):
        item_name = request.GET['id']
        item_name = str(item_name)
        cart = request.session.get('cart', {})
        cart[item_name] = item_name
        request.session['cart'] = cart
        return HttpResponse("Added Sucessfully!")

def charge(request):
    if request.method == "POST":
        form = SalePaymentForm(request.POST)
        if form.is_valid(): # charges the card
            return HttpResponse("Success! We've charged your card!")
    else:
        form = SalePaymentForm()
 
    return render(request,"mainapp/charge.html",{'form': form})