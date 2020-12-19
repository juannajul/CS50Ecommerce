from auctions.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def get_watchlist(request):
    watchlist_number=""
    if request.user.is_authenticated:
        user = request.user
        watchlist_number = WatchList.objects.filter(user_watcher=user).count()
    
        return {
            'watchlist_number': watchlist_number
        }            
    else:
        return {
            'watchlist_number': watchlist_number
        }

