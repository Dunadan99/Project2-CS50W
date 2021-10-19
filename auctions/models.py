from typing import ContextManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
    
class Auction(models.Model):
    title = models.CharField(max_length=64)
    pic = models.URLField(blank=True)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales")
    auct_category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="items")
    time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

class Bid(models.Model):
    bid_price = models.DecimalField(max_digits=20, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    rel_auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Bid of ${self.bid_price} on {self.rel_auction}'

class Comment(models.Model):
    post = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)



   
