from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):
    status_choices = ( 
        ('BOUGHT',"BOUGHT"),   
        ('NOT AVAILABLE','NOT AVAILABLE'),
        ('PENDING','PENDING'),
    )
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=25)
    quantity = models.CharField(max_length=10)
    status = models.CharField(choices = status_choices, max_length =15)
    date = models.DateField(default='YYYY-MM-DD')

    def __str__(self):
        return self.name