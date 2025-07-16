from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Book
from users.models import FavoriteBook
from reviews.models import Review

@login_required
def user_favorites(request, user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return redirect('friends_page')

    favorite_books = FavoriteBook.objects.filter(user=user)

    return render(request, 'books/favorites.html', {
        'favorite_books': favorite_books,
        'favorite_user': user,  # kimin favorileri olduğunu göstermek için
    })

@login_required
def toggle_favorite(request, book_id):
    if request.user.is_authenticated:
        favorite, created = FavoriteBook.objects.get_or_create(user=request.user, book_id=book_id)
        if not created:
            favorite.delete()
    return redirect('book_detail', book_id=book_id)


@login_required
def favorites(request):
    # Kullanıcının favori kitaplarını getir
    favorite_books = FavoriteBook.objects.filter(user=request.user)
    return render(request, 'books/favorites.html', {'favorite_books': favorite_books})

@login_required
def add_review(request, book_id):
    book = Book.objects.get(book_id=book_id)
    if request.method == "POST":
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')

        # Yeni yorum oluştur
        Review.objects.create(
            user=request.user,
            book=book,
            rating=rating,
            review_text=review_text
        )

        return redirect('book_detail', book_id=book.book_id)  # Yorum sonrası kitabın detay sayfasına geri yönlendir

    return redirect('book_detail', book_id=book.book_id)


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = FavoriteBook.objects.filter(user=request.user, book=book).exists()

    return render(request, 'books/book_detail.html', {
        'book': book,
        'is_favorite': is_favorite,
    })

def genres_page(request, genre_name):
    # BookGenre ile ilişki kurarak genre_name üzerinden filtreleme yapıyoruz
    books = Book.objects.filter(bookgenre__genre__genre_name=genre_name)
    # Eğer kitaplar doğru bir şekilde yükleniyorsa, bu kitaplar üzerinde id kontrolü yapabilirsiniz
    for book in books:
        print(f"Book: {book.title}, ID: {book.book_id}")
    return render(request, 'books/genres.html', {
        'genre_name': genre_name,
        'books': books
    })

def books(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'books/books.html', {'books': books})



