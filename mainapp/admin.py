from django.contrib import admin

from mainapp.models import Tag, Item, ItemTag, Sale, Category, Sub_Cat

# Register your models here.
admin.site.register(Tag)
admin.site.register(Item)
admin.site.register(Sub_Cat)
admin.site.register(Category)
admin.site.register(ItemTag)