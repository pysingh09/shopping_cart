from pusher import Pusher
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.defaulttags import register
from allauth.account.signals import user_logged_in
from allauth.account.signals import user_signed_up
from django.contrib.auth.decorators import login_required

from mainapp import constants
from mainapp.models import Sale,Category
from mainapp.forms import SalePaymentForm
from mainapp.models import Tag,ItemTag,Item,SubCategory,History

from dal import autocomplete


class HistoryData(View):
    def get(self,request):
        uname = request.GET['id']
        obj = History.objects.filter(username__exact=uname)
        details =[]
        for item in obj:
            details.append({'name':item.item_name,'quantity':item.quantity,'date':item.date})

        return render(request, 'mainapp/history.html', {'data':details})

historyData = login_required(HistoryData.as_view())


class Add_Fav(View):
    def get(self,request):
        uname = request.GET['uname']
        item_name = request.GET['iname']
        return HttpResponse("Added Sucessfully!")

addtofav = login_required(Add_Fav.as_view())


class ItemAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Item.objects.all()

        if self.q:
            qs = qs.filter(item_name__istartswith=self.q)

        return qs

itemauto = login_required(ItemAutocomplete.as_view())


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
        data = []
        for subcategory in subcategory:
            data.append({'name':subcategory.name,'image':"shopping_cart/"+subcategory.image.name})
        context = {'ref':data,"to_ref":True,}
        return render(request, 'mainapp/first.html', context)

allProduct = login_required(AllProduct.as_view())


class MainPage(View):
    def get(self,request):
        cat_obj = Category.objects.all()
        data = []
        for x in cat_obj:
            data.append({'name':x.name,'image':"shopping_cart/"+x.photo.name})
        context = {'ref':data,"to_ref":False}
        return render(request, 'mainapp/first.html', context)

mainPage = login_required(MainPage.as_view())

@register.filter(name='lookup')
def cut(value, arg):
    return arg


class Logic(View):
    def get(self,request):
            tags = request.GET['id']
            Itemobj = Item()
            tags = tags.split(" ")
            data = []
            quantity = request.session.get('quantity', {})
            for tag in tags:
                tag_obj = Tag.objects.filter(tag_title__icontains=tag)
                for tag in tag_obj:
                    itemtagobj = ItemTag.objects.filter(tag_id=tag.id)
                    for item in itemtagobj:
                        itemobj = Item.objects.get(id = item.item_id.id)
                        if itemobj.item_name in quantity:
                            data.append({'name':itemobj.item_name,'image':"shopping_cart/"+itemobj.photo.name,'price':str(itemobj.price),'tag':Itemobj.tag_finder(itemobj.id),'quantity':quantity[itemobj.item_name]})
                        else:
                            data.append({'name':itemobj.item_name,'image':"shopping_cart/"+itemobj.photo.name,'price':str(itemobj.price),'tag':Itemobj.tag_finder(itemobj.id),'quantity':0})
            context = {'ref':data,"to_ref":False}
            return render(request, "mainapp/itemlist.html", context)

logic = login_required(Logic.as_view())

def cartdetails(request):
        cart = request.session.get('cart', [])
        quantity = request.session.get('quantity', {})
        data, count = [],{}
        total = 0.0
        for item in cart:
            itemobj= Item.objects.get(item_name__exact=item)
            data.append({'count':quantity[itemobj.item_name],'name':itemobj.item_name,'price':str(itemobj.price),'image':'shopping_cart/'+itemobj.photo.name})
            total += itemobj.price * quantity[itemobj.item_name]
        context = {'cart':data, 'total':total}
        return context

class ViewCart(View):
    def get(self,request):
        return render(request, "mainapp/cart.html", cartdetails(request))

viewCart = login_required(ViewCart.as_view())

def count_logic(item,request,less):
    quantity = request.session.get('quantity',{})
    try:
        current_value = quantity[item]
        if less :
            if current_value > 0:
                current_value -= 1
        else:
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
        count_logic(item_name, request,False)
        request.session['cart'] = cart
        return HttpResponse("Added Sucessfully!")

addCart = login_required(AddCart.as_view())


class RemoveCart(View):
    def get(self,request):
        item_name = request.GET['id']
        cart = request.session.get('cart', {})
        cart[item_name] = item_name
        count_logic(item_name, request,True)
        request.session['cart'] = cart
        return HttpResponse("Remove Sucessfully!")

removecart = login_required(RemoveCart.as_view())

def charge(request):
    if request.method == "POST":
        form = SalePaymentForm(request.POST)
        form.amount = request.GET['id']
        if form.is_valid():
            data = cartdetails(request)
            for item in data['cart']:
                history = History()
                print item
                history.username = request.GET['uname']
                history.item_name = item['name']
                history.quantity = int(item['count'])
                history.save()

            request.session['cart'] = ""
            return redirect("/accounts/login/")
    else:
        form = SalePaymentForm()
 
    return render(request,"mainapp/charge.html",{'form': form})