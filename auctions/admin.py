from django.contrib import admin
from .models import Auction, Bid, Category, Comment, User, Watchlist

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff')

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'starting_bid', 'auct_category', 'time')

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Watchlist)
