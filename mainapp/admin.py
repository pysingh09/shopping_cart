from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from allauth.account.models import EmailAddress, EmailConfirmation

from mainapp.models import Tag, Item, ItemTag, Sale, Category, SubCategory, MyUser

admin.site.register(Tag)
admin.site.register(Item)
admin.site.register(MyUser)
admin.site.register(SubCategory)
admin.site.register(Category)
admin.site.register(ItemTag)
admin.site.unregister(Group)
admin.site.unregister(Site)
# admin.site.unregister(EmailAddress)

