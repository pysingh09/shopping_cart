from django.conf.urls import include,url
from django.views.generic import TemplateView

from mainapp import views

urlpatterns = [
    url(r'^logic/add', views.addCart, name="addtocart"),
    url(r'^logic/', views.logic, name="product"),
    url(r'^view_cart/del', views.removeItem, name="del"),
    url(r'^view_cart/', views.viewCart, name="viewcart"),
    url(r'^add_cart/', views.addCart, name="add"),
    url(r'^charge/$', views.charge, name="charge"),
    # url(r'^cat/', views.categoryList, name="cat"),
    url(r'^profile/', views.mainPage, name="home"),
    url(r'^product/', views.allProduct, name="sub_cat"),
]