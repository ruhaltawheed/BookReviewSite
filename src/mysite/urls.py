"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from users.views import (
    home_screen_view,
    registration_view,
    logout_view,
    login_view,
    top_rated_books_api,
    top_reviews_api,
    favorite_genres_api,
    friends_page,
    follow_user,
    unfollow_user,
    chat_with_friend,
)

from books.views import (
    genres_page,
    book_detail,
    add_review,
    books,
    favorites,
    toggle_favorite,
    user_favorites,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view, name="home"),
    path('register/', registration_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('friends_page/<int:user_id>/', chat_with_friend, name='chat_with_friend'),  # Bu URL'yi önce tanımlayın
    path('friends_page/', friends_page, name='friends_page'),  # Bu URL sonra olmalı
    path('follow_user/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow_user/<int:user_id>/', unfollow_user, name='unfollow_user'),
    path('api/top-rated-books/', top_rated_books_api, name='top_rated_books_api'),
    path('api/top-reviews/', top_reviews_api, name='top-reviews-api'),
    path('api/favorite-genres/', favorite_genres_api, name='favorite-genres-api'),
    path('tur/<str:genre_name>/', genres_page, name="genres"),
    path('book/<int:book_id>/', book_detail, name='book_detail'),
    path('book/<int:book_id>/add_review/', add_review, name='add_review'),
    path('book/<int:book_id>/toggle_favorite/', toggle_favorite, name='toggle_favorite'),
    path('books/', books, name="books"),
    path('favorites/', favorites, name="favorites"),
    path('favorites/<int:user_id>/', user_favorites, name='user_favorites'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
