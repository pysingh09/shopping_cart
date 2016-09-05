import stripe
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from shopping_cart import settings

class Item(models.Model):
    item_name = models.CharField(max_length = 300, unique = True)
    price = models.FloatField()
    quantity = models.IntegerField()
    photo = models.ImageField(default = "default.jpg")

    def __str__(self):
        return self.item_name

class Profile (models.Model):
    user = models.OneToOneField(User)  
    mobile = models.CharField(max_length = 300, unique = True)

    def __str__(self):  
          return "%s's profile" % self.user  

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User) 

class Category(models.Model):
    name = models.CharField(max_length=200,unique=True)
    photo = models.ImageField(default="default.jpg")

    def __str__(self):
        return self.name
        
class SubCategory(models.Model):
    p_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,unique=True)
    image = models.ImageField(default="default.jpg")

    def __str__(self):
        return self.name

class Tag(models.Model):
    tag_title = models.CharField(max_length=300,unique=True)

    def __str__(self):
        return self.tag_title

class ItemTag(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)

class Sale(models.Model):
    charge_id = models.CharField(max_length=32)

    def __init__(self, *args, **kwargs):
        super(Sale, self).__init__(*args, **kwargs)
        stripe.api_key = settings.STRIPE_API_KEY
        self.stripe = stripe
 
    def charge(self, price_in_cents, number, exp_month, exp_year, cvc):
        if self.charge_id:
            return False, Exception(message="Already charged.")
        try:
            response = self.stripe.Charge.create(
                amount = price_in_cents,
                currency = "usd",
                card = {
                    "number" : number,
                    "exp_month" : exp_month,
                    "exp_year" : exp_year,
                    "cvc" : cvc
                },
                description='Thank you for your purchase!')
            self.charge_id = response.id

        except self.stripe.CardError, ce:
            return False, ce
        return True, response
