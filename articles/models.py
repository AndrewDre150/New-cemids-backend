from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    author = models.CharField(max_length=100)
    link = models.URLField()
    image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
