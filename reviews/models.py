from django.db import models

# Create your models here.


class Review(models.Model):
    headline = models.CharField(max_length=100)
    written_review = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    production = models.ForeignKey(
        "history.History", related_name="reviews", on_delete=models.CASCADE
    )
    scan = models.ForeignKey(
        "history.HistoryScan",
        related_name="reviews",
        on_delete=models.CASCADE,
        null=True,
    )
