from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name




class Article(models.Model):
    STATUS_CHOICES = [
        ("pending", "Chờ duyệt"),
        ("approved", "Đã duyệt"),
        ("rejected", "Bị từ chối"),
    ]

    title = models.CharField(max_length=255)
    short_desc = models.CharField(max_length=500)
    content = models.TextField()
    published_at = models.DateTimeField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="articles")
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="articles")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["-published_at", "id"], name="idx_pub_id_desc"),
            models.Index(fields=["category", "-published_at", "id"], name="idx_cat_pub_desc"),
        ]
        ordering = ["-published_at", "-id"]  # mặc định mới → cũ

    def __str__(self):
        return self.title
