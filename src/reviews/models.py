from django.db import models

class Review(models.Model):
	review_id = models.AutoField(primary_key=True)
	rating = models.DecimalField(max_digits=2, decimal_places=1)
	review_text = models.TextField()
	user = models.ForeignKey("users.User", on_delete=models.CASCADE)
	book = models.ForeignKey("books.Book", on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.review_id} - {self.book} - {self.user}"

	class Meta:
		db_table = "Reviews"

class Comment(models.Model):
	comment_id = models.AutoField(primary_key=True)
	review = models.ForeignKey(Review, on_delete=models.CASCADE)
	user = models.ForeignKey("users.User", on_delete=models.CASCADE)
	comment_text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.comment_id} - {self.review} - {self.user}"

	class Meta:
		db_table = "Comments"

class Report(models.Model):
	report_id = models.AutoField(primary_key=True)
	user = models.ForeignKey("users.User", on_delete=models.CASCADE)
	review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, blank=True)
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
	report_reason = models.TextField()
	reported_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.report_id} - {self.user}"

	class Meta:
		db_table = "Reports"

