from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import constraints
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, widgets

from .models import Auction, User


def index(request):
    return render(request, "auctions/index.html")


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
        labels = { 'starting_bid' : 'Price', 'auct_category' : 'Category', 'pic' : 'Picture URL'}
        widgets = { 'description' : widgets.Textarea(attrs={'cols' : 30, 'rows' : 4}), 
                    'starting_bid' : widgets.NumberInput(attrs={'min' : 0, 'value' : 0.0})}

def create_listing(request):

    if request.method == 'POST':
        pass

    form = CreateForm()
    return render(request, "auctions/create_listing.html", {
        "form": form 
    })
    
