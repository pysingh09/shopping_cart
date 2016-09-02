from django.conf.urls import include,url
from django.views.generic import TemplateView

from mainapp import views

urlpatterns = [
    url(r'^logic/add', views.addcart, name="addtocart"),
    url(r'^logic/', views.logic, name="product"),
    url(r'^view_cart/del', views.removeitem, name="del"),
    url(r'^view_cart/', views.viewcart, name="viewcart"),
    url(r'^add_cart/', views.addcart, name="add"),
    url(r'^charge/$', views.charge, name="charge"),
    url(r'^cat/', views.categorylist, name="cat"),
    url(r'^profile/', views.mainpage),
    url(r'^product/', views.allproduct, name="sub_cat"),
]