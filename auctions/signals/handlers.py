from django.db.models.signals import post_delete
from auctions.models import Bid,Auction
from django.dispatch import receiver

@receiver(post_delete, sender=Bid)
def on_delete(sender, **kwargs):
    for item in Auction.objects.all():
        item.upd_price()