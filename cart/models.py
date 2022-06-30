import secrets
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
#from credo.payment import Payment
#from core.models import InPayCustomer
from django.shortcuts import reverse
from .payment import Payment



User = get_user_model()

#payment = Payment(public_key='settings.ETRANZACT_PUBLIC_KEY', secret_key='settings.ETRANZACT_SECRET_KEY')


class Address(models.Model):
    ADDRESS_CHOICES = (
        ('B', 'Billing'),
        ('S', 'Shipping'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.address_line_1}, {self.address_line_2}, {self.city} {self.zip_code}"
    
    
class Meta:
    verbose_name_plural = 'Addresses'
    
    
class ColourVariation(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    
class SizeVariation(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='product_images')
    description = models.TextField()
    price = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    available_colours = models.ManyToManyField(ColourVariation)
    available_sizes = models.ManyToManyField(SizeVariation)
    
    def __str__(self):
        return self.title
    
    
    def get_absolute_url(self):
        return reverse("cart:product-detail", kwargs={'slug': self.slug})
    
    def get_update_url(self):
        return reverse("merchant:product-update", kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse("merchant:product-delete", kwargs={'pk': self.pk})
    
    def get_price(self):
        return "{:.2f}".format(self.price / 100)
    
class OrderItem(models.Model):
    order = models.ForeignKey("Order", related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    colour = models.ForeignKey(ColourVariation, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeVariation, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
    
    def get_raw_total_item_price(self):
        return self.quantity * self.product.price
    
    def get_total_item_price(self):
        price = self.get_raw_total_item_price() # raw format of 1000
        return "{:.2f}".format(price / 100)
    
    
class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    #payment = models.ForeignKey("Payment", on_delete=models.CASCADE, related_name="paid_intent", blank=True, null=True)
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        Address, related_name='billing_address', blank=True, null=True, on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', blank=True, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.reference_number
    
    @property
    def reference_number(self):
        return f"ORDER-{self.pk}"
    
    def get_raw_subtotal(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_raw_total_item_price()
        return total
    
    def get_customer_name(self):
        customer_name = ""
        for customer in self.customerorder.all():
            customer_name = customer.customer_name
        return customer_name
    
    
    def get_customer_email(self):
        email = ""
        for customer in self.customerorder.all():
            email = customer.email
        return email
    
    def get_customer_phone_number(self):
        phone_number = ""
        for customer in self.customerorder.all():
            phone_number = customer.phone_number
        return phone_number
    
    def get_subtotal(self):
        subtotal = self.get_raw_subtotal()
        return "{:.2f}".format(subtotal / 100)
    
    def get_raw_total(self):
        subtotal = self.get_raw_subtotal()
        # add tax, add delivery, subtract discounts
        # total = subtotal -discount + tax + add delivery 
        return subtotal
    
    def get_total(self):
        total  = self.get_raw_total()
        return "{:.2f}".format(total / 100)
    
    
class Payment(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name="intent")
    amount = models.FloatField()
    ref = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.ref
    
   # @property
    #def reference_number(self):
    #    return f"PAYMENT-{self.order}-{self.pk}"
    
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)
        
    def get_amount(self):
        amount = 0
        for order in self.paid_intent.all():
            amount = order.get_total()
        return amount
    
    def verify_payment(self):
        payment = Payment()
        status, verify_payment = payment.verify_payment(self.ref, self.amount)
        if status:
            if verify_payment['amount'] == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False

    
    def pre_save_product_receiver(sender, instance, *args, **kwargs):
        if not instance.slug:
            instance.slug = slugify(instance.title)
            
    pre_save.connect(pre_save_product_receiver, sender=Product)
    
    
    

    
    
    
    