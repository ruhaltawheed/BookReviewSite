from django.contrib import admin
from .models import User, UserFollower, FavoriteBook, ReadingProgress

admin.site.register(User)
admin.site.register(UserFollower)
admin.site.register(FavoriteBook)
admin.site.register(ReadingProgress)
