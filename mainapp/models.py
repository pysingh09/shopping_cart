import stripe

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from shopping_cart import settings


class MyUserManager(BaseUserManager):

    def create_user(self, email, mobile_number, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=MyUserManager.normalize_email(email),
            mobile_number=mobile_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile_number, password):
        u = self.create_user(email,
                        password=password,
                        mobile_number=mobile_number
                    )
        u.is_admin = True
        u.save(using=self._db)
        return u


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=50, default="none")
    email = models.EmailField(
                        verbose_name='email address',
                        max_length=255,
                        unique=True,
                    )
    mobile_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_number']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

class Item(models.Model):
    item_name = models.CharField(max_length=300, unique=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    photo = models.ImageField(default = "default.jpg")

    def __str__(self):
        return self.item_name

    def tag_finder(self, item_id):
        itemtagobj = ItemTag.objects.filter(item_id=item_id)
        tags=""
        for tag in itemtagobj:
            tagobj = Tag.objects.get(id = tag.tag_id.id)
            tags += tagobj.tag_title+" "
        return tags


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    photo = models.ImageField(default="default.jpg")

    def __str__(self):
        return self.name
        
class SubCategory(models.Model):
    categoryid = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(default="default.jpg")

    def __str__(self):
        return self.name

class Tag(models.Model):
    tag_title = models.CharField(max_length=300, unique=True)

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
