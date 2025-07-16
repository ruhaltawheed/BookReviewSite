from django.db import models

class Book(models.Model):
	book_id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=255)
	publication_year = models.IntegerField()
	description = models.TextField(null=True, blank=True)
	cover_images = models.ImageField(upload_to='covers/', blank=True, null=True)
	
	def __str__(self):
		return self.title

	class Meta:
		db_table = "Books"

class Author(models.Model):
	author_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	surname = models.CharField(max_length=100)

	def __str__(self):
		return f"{self.name} {self.surname}"

	class Meta:
		db_table = "Authors"

class BookAuthor(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.author} - {self.book}"

	class Meta:
		db_table = "Book_Authors"
		unique_together = ("book", "author")

class Genre(models.Model):
	genre_id = models.AutoField(primary_key=True)
	genre_name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.genre_name

	class Meta:
		db_table = "Genres"

class BookGenre(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.genre} - {self.book}"

	class Meta:
		db_table = "Book_Genres"
		unique_together = ("book", "genre")

