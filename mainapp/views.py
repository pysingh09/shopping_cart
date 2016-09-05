from pusher import Pusher
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from allauth.account.signals import user_logged_in
from allauth.account.signals import user_signed_up
from django.contrib.auth.decorators import login_required

from mainapp import constants
from mainapp.models import Sale,Category
from mainapp.forms import SalePaymentForm
from mainapp.models import Tag,ItemTag,Item,SubCategory


class RemoveItem(View):

    def get(self,request):
        name=request.GET['id']
        if name in request.session['cart']:
            request.session['cart'].remove(name)
            request.session['cart'] = request.session['cart']
        else:
            return HttpResponse("Failed!")
        return HttpResponse("a:b")

removeitem = login_required(RemoveItem.as_view())

class AllProduct(View):

    def get(self,request):
        req_category= request.GET['id']
        category = Category.objects.get(name=req_category)
        category_id = category.id
        subcategory = SubCategory.objects.filter(p_id=category_id)
        photo,name = [],[]
        for subcategory in subcategory:
            name.append(subcategory.name)
            photo.append("shopping_cart/"+subcategory.image.name)
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
        req_category = request.GET['id']
        context = {'ref':cat,"to_ref":True,'t':req_category}
        return render(request, "mainapp/first.html", context)

categorylist = login_required(CategoryList.as_view())

def tag_finder(item_id):
    itemtagobj = ItemTag.objects.filter(item_id=item_id)
    tags=""
    for tag in itemtagobj:
        tagobj = Tag.objects.get(id = tag.tag_id.id)
        tags += tagobj.tag_title+" "
    return tags

class Logic(View):

    def get(self,request):
            tags = request.GET['id']
            tags=tags.split(" ")
            itemlist,pricelist,photo,tags_on_item = [],[],[],[]
            for tag in tags:
                tag_obj = Tag.objects.filter(tag_title__icontains=tag)
                for tag in tag_obj:
                    itemtagobj = ItemTag.objects.filter(tag_id=tag.id)
                    for item in itemtagobj:
                        itemobj = Item.objects.get(id = item.item_id.id)
                        itemlist.append(itemobj.item_name)
                        pricelist.append(itemobj.price)
                        photo.append("shopping_cart/"+itemobj.photo.name)
                        '''getting  Tags releted to each itmes'''
                        tags_on_item.append(tag_finder(itemobj.id))
            price = iter(pricelist)
            photo = iter(photo)
            tags_on_item=iter(tags_on_item)
            context = {'ref':itemlist,"to_ref":False,"p":price,'photo':photo,'tags':tags_on_item}
            return render(request, "mainapp/itemlist.html", context)

logic = login_required(Logic.as_view())

class Cart(View):

    def get(self,request):
        itemname = request.GET['id']

cart = login_required(Cart.as_view())

class ViewCart(View):

    def get(self,request):
        cart = request.session.get('cart', [])
        price,image = [],[]
        total = 0.0
        for item in cart:
            itemobj= Item.objects.get(item_name__exact=item)
            image.append('shopping_cart/'+itemobj.photo.name)
            price.append(itemobj.price)
            total += itemobj.price
        price = iter(price)
        image = iter(image)
        context = {'cart':cart,'price':price,'total':total,'image':image}
        return render(request, "mainapp/cart.html", context)

viewcart = login_required(ViewCart.as_view())

class AddCart(View):
    
    def get(self,request):
        item_name = request.GET['id']
        cart = request.session.get('cart', [])
        cart.append(item_name)
        request.session['cart'] = cart
        return HttpResponse("Added Sucessfully!")

addcart = login_required(AddCart.as_view())

def charge(request):
    if request.method == "POST":
        form = SalePaymentForm(request.POST)
        form.amount = request.GET['id']
        if form.is_valid():
            request.session['cart'] = ""
            return redirect("/accounts/login/")
    else:
        form = SalePaymentForm()
 
    return render(request,"mainapp/charge.html",{'form': form})