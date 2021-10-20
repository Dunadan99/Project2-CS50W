from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import constraints
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, widgets

from .models import Auction, Category, User, Bid


def index(request):
    act_listings = Auction.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {"listings" : act_listings})


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

    form = CreateForm()
    return render(request, "auctions/create_listing.html", {
        "form": form
    })

def listing(request, id):
    return render(request, "auctions/listing.html")

def categories(request):
    list_cat = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories" : list_cat})

def category(request, id):
    categ = Category.objects.get(id=id)
    categ_aucts = categ.items.all()
    return render(request, 'auctions/category.html', {"category" : categ , "listings" : categ_aucts})
    
