from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model


User = get_user_model()
      
        
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.user.username}"


def post_save_user_receiver(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


post_save.connect(post_save_user_receiver, sender=User) 
        


 
