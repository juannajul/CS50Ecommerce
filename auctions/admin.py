from django.contrib import admin
from .models import User, Auction, Bid, Category, Comment, WatchList

class PageAuction(admin.ModelAdmin):
    readonly_fields = ('created_at', 'closed_on', 'winner')
    search_fields = ('title', 'user_creator__username')
    list_filter = ('category__category','active')
    list_display = ('title', 'user_creator', 'active')
    list_display_links = ('title',)
    ordering = ('id',)

class PageBid(admin.ModelAdmin):
    readonly_fields = ('date_bid',)
    list_display = ('id', 'user_bidder', 'bid','auction_bided', 'date_bid')
    list_filter = ('user_bidder', 'auction_bided')
    search_fields = ('user_bidder__username', 'auction_bided__title')
    ordering = ('bid',)

class PageCategory(admin.ModelAdmin):
    list_display = ('id', 'category')

class PageComment(admin.ModelAdmin):
    readonly_fields = ('comment_date', )
    list_display = ('id', 'auction_commented', 'user_comment')
    ordering = ('-comment_date',)
    list_filter = ('user_comment',)
    list_display_links = ('auction_commented',)
    

class PageWatchlist(admin.ModelAdmin):
    list_display = ('id', 'user_watcher', 'auction_watched')
    list_display_links =( 'user_watcher', 'auction_watched')
    list_filter = ('user_watcher',)

# Register your models here.
admin.site.register(User)
admin.site.register(Auction, PageAuction)
admin.site.register(Bid, PageBid)
admin.site.register(Category, PageCategory)
admin.site.register(Comment, PageComment)
admin.site.register(WatchList, PageWatchlist)