from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("addWatchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("deleteWatchlist/<int:listing_id>", views.delete_watchlist, name="delete_watchlist"),
    path("watchlistPage", views.watchlist_page, name="watchlist_page"),
    path("comment/<int:listing_id>", views.comment, name="new_comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category_search, name="category_search"),
    path("close/<int:listing_id>", views.close_listing, name="close")
]
