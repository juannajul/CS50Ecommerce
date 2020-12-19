from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *
from django.contrib import messages
import datetime
from .models import *
from django.contrib.auth.decorators import login_required


def index(request):
    auctions = Auction.objects.all()
    return render(request, "auctions/index.html", {
        "auctionListing": auctions
    })


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

@login_required(login_url='login')
def create_listing(request):
    categories = Category.objects.all()
    if request.method == "POST":
        createForm = FormCreateArticule(request.POST)
        if createForm.is_valid():
            titleField = createForm.cleaned_data["title"]
            descriptionField = createForm.cleaned_data["description"]
            initialBidField = createForm.cleaned_data["bid_initial"]
            imageField = createForm.cleaned_data["image_url"]
            categoryField = createForm.cleaned_data["category"]
            categoryName = categories[categoryField - 1].category
            categoryInstance = Category.objects.get(pk=categoryField)

            auction = Auction.objects.create(
                title=titleField,
                description=descriptionField,
                bid_initial=initialBidField,
                image_url=imageField,
                category=categoryInstance,
                user_creator=request.user
            )

            first_bid = Bid.objects.create(
                bid=initialBidField, user_bidder=request.user, auction_bided=auction)
            first_bid.save()
            auction.save()
            messages.success(
                request, f'You have created successfully your auction: {titleField}, for ${initialBidField}')
            return redirect('create_listing')

    return render(request, "auctions/create_listing.html", {
        'createForm': FormCreateArticule()
    })


def listing(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)
    watchList = None
    comments = Comment.objects.filter(auction_commented=listing_id)
    winner = None
    winner = listing.winner
    noneInitialBid = Bid.objects.filter(auction_bided=listing_id).exists()
    if noneInitialBid == False:
        currentBid = Bid(
                    bid=listing.bid_initial,
                    user_bidder=listing.user_creator,
                    auction_bided=listing
                )
        currentBid.save()
    if request.user.is_authenticated:
        user = request.user
        watchList = WatchList.objects.filter(
            auction_watched=listing_id, user_watcher=user)
        if winner == request.user:
            messageInfo = messages.info(request, f'Your are the winner of this auction')
        elif winner != request.user and winner != None:
            messageInfo = messages.info(request, f'\"{winner.username.capitalize()}\" is the winner of this auction')
            
    bids = listing.auction_bided.count() - 1
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bidForm": FormBid(),
        "watchlist": watchList,
        "commentForm": FormComment(),
        "comments":comments,
        "bids":bids,
        "winner":winner
    })


@login_required(login_url='login')
def bid(request, id):
    listing = Auction.objects.get(pk=id)
    if request.method == "POST":
        bidForm = FormBid(request.POST)
        if bidForm.is_valid():
            listing_id = id
            newBid = bidForm.cleaned_data["new_bid"]
            bidAuction = Bid.objects.filter(auction_bided=listing_id).last()
            bids = Bid.objects.filter(auction_bided=listing_id).count()
            nonInitialBid = Bid.objects.filter(auction_bided=listing_id).exists()
            currentBid = bidAuction.bid 
            if bids == 1 and newBid >= currentBid:
                newCurrentBid = Bid(
                    bid=newBid,
                    user_bidder=request.user,
                    auction_bided=listing
                )
                newCurrentBid.save()
                messageSuccess = messages.success(
                    request, f'You have made your Bid for {listing.title} of ${newBid}')
                return redirect('listing', listing_id=id)
            elif newBid > currentBid:
                newCurrentBid = Bid(
                    bid=newBid,
                    user_bidder=request.user,
                    auction_bided=listing
                )
                newCurrentBid.save()
                messageSuccess = messages.success(
                    request, f'You have made your Bid for {listing.title} of ${newBid}')
                return redirect('listing', listing_id=id)
            else:
                messageWarning = messages.warning(
                    request, f'Your bid must be greater than ${currentBid}')
                return redirect('listing', listing_id=id)
        else:
            return redirect('index')
    else:
        return redirect('index')


@login_required(login_url='login')
def add_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Auction.objects.get(pk=listing_id)
        newWatchList = WatchList(
            user_watcher=request.user, auction_watched=listing)
        newWatchList.save()
        messagesSuccess = messages.success(
            request, f"You have added this item to the watchlist.")
        return redirect('listing', listing_id=listing_id)
    else:
        return redirect('index')


@login_required(login_url='login')
def delete_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Auction.objects.get(pk=listing_id)
        deleteWatchList = WatchList.objects.filter(
            auction_watched=listing_id, user_watcher=request.user)
        deleteWatchList.delete()
        messagesSuccess = messages.success(
            request, f"You have deleted this item successfully from your watchlist")
        return redirect('listing', listing_id=listing_id)
    else:
        return redirect('index')

@login_required(login_url='login')
def watchlist_page(request):
    listing_list = []
    auction_list = []
    total = 0
    counter = 0
    watching_items = request.user.watcher.all()
    for w in watching_items:
        listing_list.append(w)
        a = w.auction_watched_id
        auction = Auction.objects.get(pk=a)
        auction_list.append(auction)
        total += float(auction.auction_bided.last().bid)
        counter += 1
    return render(request, "auctions/watchlist.html",{
        "a":auction_list,
        "total":total,
        "counter": counter
    })

@login_required(login_url='login')
def comment(request, listing_id):
    if request.method == "POST":
        listing = Auction.objects.get(pk=listing_id)
        commentForm = FormComment(request.POST)
        if commentForm.is_valid():
            commentField = commentForm.cleaned_data["new_comment"]
            commentator = request.user
            comment = Comment(
                comment=commentField,
                auction_commented=listing,
                user_comment=commentator
                )
            comment.save()
            messageSuccess = messages.success(
                    request, f'You have commented')
            return redirect('listing', listing_id=listing_id)
    return redirect('index')

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories":categories
    })

def category_search(request, category_id):
    category = Category.objects.get(pk=category_id)
    listing = Auction.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "auctionListing": listing
    })

@login_required(login_url='login')
def close_listing(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)
    bids = Bid.objects.filter(auction_bided=listing_id).count()
    if request.method == "POST":
        if listing.user_creator.id == request.user.id and bids > 1:
            userWinner = listing.auction_bided.last().user_bidder
            listing.winner = userWinner
            listing.closed_on = datetime.datetime.now()
            listing.active = False
            listing.save()
            
            return redirect('listing', listing_id=listing_id)
            
        else:
            messageWarning = messages.warning(request, f'There is no winner')
            return redirect('listing', listing_id=listing_id)
    return redirect('index')
