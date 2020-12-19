from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
    def __str__(self):
        return self.username


class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id} {self.category}"

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=264)
    bid_initial = models.DecimalField(max_digits=12, decimal_places=2)
    image_url = models.URLField(blank=True, default="https://www.salonlfc.com/wp-content/uploads/2018/01/image-not-found-scaled-1150x647.png")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auctions_product")
    user_creator = models.ForeignKey(User, on_delete=models.CASCADE , related_name="creator")
    created_at = models.DateTimeField(auto_now_add=True)
    closed_on = models.DateTimeField(auto_now=False, blank=True, null=True)
    active = models.BooleanField(default=True, verbose_name="is_active")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="user_winner")

    def __str__(self):
        return f"{self.title} {self.bid_initial} {self.user_creator} {self.created_at}"

class Bid(models.Model):
    bid = models.DecimalField(max_digits=12, decimal_places=2)
    user_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    auction_bided = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_bided")
    date_bid = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user_bidder} {self.auction_bided} {self.bid}"
    class Meta:
        ordering = ['bid']

class Comment(models.Model):
    comment = models.TextField(max_length=264)
    auction_commented = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_commented")
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_comment} {self.auction_commented} {self.comment} {self.comment_date}"

class WatchList(models.Model):
    user_watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")
    auction_watched = models.ForeignKey(Auction, blank=True, on_delete=models.CASCADE, related_name= "watched")

    def __str__(self):
        return f"{self.user_watcher} {self.auction_watched}"
