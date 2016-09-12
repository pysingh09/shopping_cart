from django.conf.urls import include,url
from django.views.generic import TemplateView

from mainapp import views

urlpatterns = [
    url(r'^logic/removetocart', views.removecart, name="removetocart"),
    url(r'^logic/addtofav', views.addtofav, name="addtofav"),
    url(r'^logic/add', views.addCart, name="addtocart"),
    url(r'^logic/', views.logic, name="product"),
    url(r'^view_cart/del', views.removeItem, name="del"),
    url(r'^view_cart/', views.viewCart, name="viewcart"),
    url(r'^add_cart/', views.addCart, name="add"),
    url(r'^charge/$', views.charge, name="charge"),
    url(r'^profile/', views.mainPage, name="home"),
    url(r'^product/', views.allProduct, name="sub_cat"),
    url(r'^history/', views.historyData, name="history"),
    url(r'^item-autocomplete/$',views.itemauto ,name='item-auto',)
]