from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, AccountAuthenticationForm
from django.db.models import Avg, Prefetch, Q
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from books.models import Book, Genre, BookGenre
from reviews.models import Review
from .models import User, UserFollower, Message

import random

def home_screen_view(request):
    context = {}

    return render(request, "users/home.html", context)

@login_required
def chat_with_friend(request, user_id):
    try:
        friend = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return redirect('friends_page')  # Kullanıcı bulunamazsa ana sayfaya yönlendir.


    # Mesajları al
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=friend)) | (Q(sender=friend) & Q(receiver=request.user))
    ).order_by('timestamp')

    # Yeni mesaj gönderme işlemi
    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            Message.objects.create(sender=request.user, receiver=friend, content=content)

    return render(request, 'users/chat_with_friend.html', {
        'friend': friend,
        'messages': messages
    })

@login_required
def friends_page(request):
    User = get_user_model()

    query = request.GET.get('q', '')

    following = UserFollower.objects.filter(follower=request.user)
    followers = UserFollower.objects.filter(following=request.user)

    users = User.objects.exclude(user_id=request.user.user_id)

    if query:
        users = users.filter(username__icontains=query)

    followed_user_ids = set(following.values_list('following__user_id', flat=True))

    return render(request, 'users/friends_page.html', {
        'following': following,
        'followers': followers,
        'users': users,
        'query': query,
        'followed_user_ids': followed_user_ids,
    })

@login_required
def follow_user(request, user_id):
    user_to_follow = User.objects.get(user_id=user_id)
    
    if user_to_follow != request.user:
        # Kullanıcıyı takip et
        UserFollower.objects.get_or_create(follower=request.user, following=user_to_follow)
    
    return redirect('friends_page')

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = User.objects.get(user_id=user_id)
    
    if user_to_unfollow != request.user:
        # Takipten çık
        UserFollower.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    
    return redirect('friends_page')


def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			users = authenticate(email=email, password=raw_password)
			login(request, users)
			return redirect('home')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'users/register.html', context)

def logout_view(request):
	logout(request)
	return redirect('home')

def login_view(request):

	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect("home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form
	return render(request, 'users/login.html', context)

def top_rated_books_api(request):
    books_with_ratings = Book.objects.annotate(avg_rating=Avg('review__rating'))
    high_rated_books = books_with_ratings.filter(avg_rating__gte=3.5).order_by('-avg_rating')[:5]

    data = [
        {
            "title": book.title,
            "image_url": book.cover_images.url if book.cover_images else "/static/img/book_sample.png"
        }
        for book in high_rated_books
    ]

    return JsonResponse(data, safe=False)

def top_reviews_api(request):
    top_reviews = Review.objects.select_related('user', 'book') \
                                 .order_by('-rating')[:10]

    data = [
        {
            "username": review.user.username,
            "book_title": review.book.title,
            "rating": float(review.rating),
            "review_text": review.review_text
        }
        for review in top_reviews
    ]
    return JsonResponse(data, safe=False)


def favorite_genres_api(request):
    genres = Genre.objects.order_by('genre_name')  # Alfabetik sırada tüm türler
    data = [{"genre_name": genre.genre_name} for genre in genres]
    return JsonResponse(data, safe=False)


