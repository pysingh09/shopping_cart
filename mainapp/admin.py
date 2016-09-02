from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from allauth.account.models import EmailAddress, EmailConfirmation

from mainapp.models import Tag, Item, ItemTag, Sale, Category, Sub_Cat

# Register your models here.
admin.site.register(Tag)
admin.site.register(Item)
admin.site.register(Sub_Cat)
admin.site.register(Category)
admin.site.register(ItemTag)
admin.site.unregister(Group)
admin.site.unregister(Site)
# admin.site.unregister(EmailAddress)

