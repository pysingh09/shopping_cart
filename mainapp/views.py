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
            del request.session['cart'][name]
            del request.session['quantity'][name]
            request.session['quantity'] = request.session['quantity']
            request.session['cart'] = request.session['cart']
        else:
            return HttpResponse("Failed!")
        return HttpResponse("")

removeItem = login_required(RemoveItem.as_view())

class AllProduct(View):

    def get(self,request):
        req_category= request.GET['id']
        category = Category.objects.get(name=req_category)
        category_id = category.id
        subcategory = SubCategory.objects.filter(categoryid=category_id)
        photo,name = [],[]
        for subcategory in subcategory:
            name.append(subcategory.name)
            photo.append("shopping_cart/"+subcategory.image.name)
        photo = iter(photo)
        context = {'ref':name,"to_ref":True,'t':id,"photo":photo}
        return render(request, 'mainapp/first.html', context)

allProduct = login_required(AllProduct.as_view())

class MainPage(View):

    def get(self,request):
        cat_obj = Category.objects.all()
        photo, name = [], []
        for x in cat_obj:
            name.append(x.name)
            photo.append("shopping_cart/"+x.photo.name)
        photo = iter(photo)
        context = {'ref':name,"to_ref":False,'t':"MainCategories","photo":photo}
        return render(request, 'mainapp/first.html', context)

mainPage = login_required(MainPage.as_view())
       
# class CategoryList(View):

#     def get(self,request):
#         req_category = request.GET['id']
#         context = {'ref':cat,"to_ref":True,'t':req_category}
#         return render(request, "mainapp/first.html", context)

# categoryList = login_required(CategoryList.as_view())

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
            itemlist, pricelist, photo, tags_on_item, count = [], [], [], [], []
            quantity = request.session.get('quantity', {})
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
                        '''getting count on each item '''
                        if itemobj.item_name in quantity:
                            count.append(quantity[itemobj.item_name])
                        else:
                            count.append("")
            price = iter(pricelist)
            photo = iter(photo)
            tags_on_item=iter(tags_on_item)
            count = iter(count)
            context = {'ref':itemlist,"to_ref":False,"p":price,'photo':photo,'tags':tags_on_item,'count':count}
            return render(request, "mainapp/itemlist.html", context)

logic = login_required(Logic.as_view())

class Cart(View):

    def get(self,request):
        itemname = request.GET['id']

cart = login_required(Cart.as_view())

class ViewCart(View):

    def get(self,request):
        cart = request.session.get('cart', [])
        quantity = request.session.get('quantity', {})
        price,image,count = [],[],[]
        total = 0.0
        for key, value in quantity.iteritems() :
            count.append(value)

        for item in cart:
            itemobj= Item.objects.get(item_name__exact=item)
            image.append('shopping_cart/'+itemobj.photo.name)
            price.append(itemobj.price)
            total += itemobj.price
        price = iter(price)
        image = iter(image)
        count = iter(count)
        context = {'cart':cart,'price':price,'total':total,'image':image,'count':count}
        return render(request, "mainapp/cart.html", context)

viewCart = login_required(ViewCart.as_view())

def count_logic(item,request):
    quantity = request.session.get('quantity',{})
    try:
        current_value = quantity[item]
        current_value += 1
        quantity[item] = current_value
        request.session['quantity'] = quantity
    except:
        quantity[item] = 1
        request.session['quantity'] = quantity
    print request.session['quantity']


class AddCart(View):
    
    def get(self,request):
        item_name = request.GET['id']
        cart = request.session.get('cart', {})
        cart[item_name] = item_name
        count_logic(item_name, request)
        request.session['cart'] = cart
        return HttpResponse("Added Sucessfully!")

addCart = login_required(AddCart.as_view())

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