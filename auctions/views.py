from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import constraints
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, widgets

from .models import Auction, Category, User, Bid, Watchlist, Comment


def index(request):
    var = { "listings" : Auction.objects.filter(is_active=True)}
    if request.user.is_authenticated:
        var["watch_number"] = Watchlist.objects.filter(user=request.user).count()
    return render(request, "auctions/index.html", var)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class CreateForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'starting_bid', 'pic', 'auct_category']
        widgets = { 'description' : widgets.Textarea(attrs={'cols' : 30, 'rows' : 4, 'class' : 'textarea'}), 
                    'starting_bid' : widgets.NumberInput(attrs={'min' : 0, 'value' : 0.0, 'class' : 'input'}),
                    'title' : widgets.TextInput(attrs={'class' : 'input'}), 'pic' : widgets.URLInput(attrs={'class' : 'input'})}


@login_required(login_url="login")
def create_listing(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            kwargs = {
                'seller' : request.user,
                'title' : form.cleaned_data['title'],
                'description' : form.cleaned_data['description'],
                'starting_bid' : form.cleaned_data['starting_bid'],
                'pic' : form.cleaned_data['pic'],
                'auct_category' : form.cleaned_data['auct_category']
            }
            if kwargs['pic'] == '':
                kwargs['pic'] = 'https://icons-for-free.com/iconfiles/png/512/market+basket+shopping+basket+store+icon+icon-1320085906374523217.png'
            
            if len(str(kwargs['description'])) >= 90:
                kwargs['desc_short'] = str(kwargs['description'])[:85].strip() + '...'
            else:
                kwargs['desc_short'] = str(kwargs['description'])

            auct = Auction(**kwargs)
            auct.save()

            kwargs = {
                'bidder' : request.user,
                'bid_price' : form.cleaned_data['starting_bid'],
                'rel_auction' : auct
            }
            bid = Bid(**kwargs)
            bid.save()

            return HttpResponseRedirect(reverse("index"))     
        else:
            var = {"watch_number" : Watchlist.objects.filter(user=request.user).count(), "form" : form}
            return render(request, "auctions/create_listing.html", var)    

    form = CreateForm()    
    var = {"watch_number" : Watchlist.objects.filter(user=request.user).count(), "form" : form}
    return render(request, "auctions/create_listing.html", var)

def listing(request, id):

    if request.method == 'POST':
        action = request.POST['action']

        if action == 'Remove from watchlist':
            Watchlist.objects.filter(id=request.POST['watch_id']).delete()
        elif action == 'Add to watchlist':
            kwargs = {'user' : request.user, 'listing' : Auction.objects.get(id=request.POST['listing'])}
            item = Watchlist(**kwargs)
            item.save()
        elif action == 'Close listing':
            listing = Auction.objects.get(id=request.POST['listing'])
            listing.is_active = False
            listing.save()
        elif action == 'Place bid':
            new_bid = request.POST['bid']
            listing = Auction.objects.get(id=request.POST['listing'])
            kwargs = {'bidder' : request.user, 'bid_price' : new_bid, 'rel_auction' : listing}
            bid = Bid(**kwargs)
            bid.save()            
            listing.starting_bid = new_bid
            listing.save()
        elif action == 'Delete':
            Comment.objects.filter(id=request.POST['comment_id']).delete()
        elif action == 'Post your comment':
            auct = Auction.objects.get(id=request.POST['listing'])
            kwargs = {'post' : auct, 'author' : request.user, 'content' : request.POST['comment']}
            comment = Comment(**kwargs)
            comment.save()


    auct = Auction.objects.get(id=id)
    comments = auct.comments.all()
    winner_bid = auct.bids.order_by('-bid_price').first()
    var = {"auct" : auct, "comments" : comments, 'winner_bid' : winner_bid}
    if request.user.is_authenticated:
        var["watch_number"] = Watchlist.objects.filter(user=request.user).count()
        watchlist = Watchlist.objects.filter(user=request.user).only('listing')
        var['in_watchlist'] = False
        for item in watchlist:
            if item.listing == auct:
                var['in_watchlist'] = True
                var['item'] = item
                break

    return render(request, "auctions/listing.html", var)

def categories(request):
    var = {'categories' : Category.objects.all()}
    if request.user.is_authenticated:
        var['watch_number'] = Watchlist.objects.filter(user=request.user).count()
    return render(request, "auctions/categories.html", var)

def category(request, id):
    categ = Category.objects.get(id=id)
    categ_aucts = categ.items.all().filter(is_active=True)
    var = {"category" : categ , "listings" : categ_aucts}
    if request.user.is_authenticated:
        var['watch_number'] = Watchlist.objects.filter(user=request.user).count()
    return render(request, 'auctions/category.html', var)

@login_required(login_url="login")
def watchlist(request):
    listing = Watchlist.objects.filter(user=request.user).only('listing')
    var = {"watch_number" : Watchlist.objects.filter(user=request.user).count(),
            "items" : listing}
    return render(request, "auctions/watchlist.html", var)
    
