from django.conf.urls import include,url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from mainapp import views
from mainapp.views import Logic,CategoryList,FirstScreen,ProductAll,Delete_From_Cart
from mainapp.views import Add_to_cart,View_cart

urlpatterns = [
    url(r'^logic/add', login_required(Add_to_cart.as_view()), name="addtocart"),
    url(r'^logic/', login_required(Logic.as_view()), name="product"),
    url(r'^view_cart/', login_required(View_cart.as_view()), name="viewcart"),
    url(r'^add_cart/', login_required(Add_to_cart.as_view()), name="add"),
    url(r'^charge/$', login_required(views.charge), name="charge"),
    url(r'^cat/', login_required(CategoryList.as_view()), name="cat"),
    url(r'^profile/', login_required(FirstScreen.as_view())),
    url(r'^product/', login_required(ProductAll.as_view()), name="sub_cat"),
    url(r'^delete/', login_required(Delete_From_Cart.as_view()), name="del"),
]