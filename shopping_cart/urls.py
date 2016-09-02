from django.contrib import admin
from django.conf import settings
from django.conf.urls import include,url
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^home/', include('mainapp.urls')),
    url(r'^$', RedirectView.as_view(url='/accounts/login'),name="login"),

] 
