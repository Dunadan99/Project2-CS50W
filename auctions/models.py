from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    list_display = ('username', 'is_staff')
    
class Auction(models.Model):
    title = models.CharField(max_length=64)
    pic = models.URLField()
    description = models.TextField
    starting_bid = models.IntegerField()
    seller = models.ManyToManyField(User, related_name="")
    

class Bid(models.Model):
    starting_price = models.IntegerField
    bidder = models.ManyToManyField(User, related_name="bids")
    rel_auction = models.ManyToManyField(Auction)

class Comment(models.Model):
    pass
   
