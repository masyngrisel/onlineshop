from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from django.db.models import Avg
from django.contrib.auth.models import User

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Report.Status.PUBLISHED)
    
    
class Report(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    
    CATEGORY_CHOICES = [
        ('BRK', 'Breakfast'),
        ('LCH', 'Lunch'),
        ('DIN', 'Dinner'),
        ('DES', 'Dessert'),
        ('APP', 'Appetizer'),
    ]
        
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipe_reports"
    )
    body = models.TextField()
    image = models.ImageField(upload_to='reports/', null=True, blank=True)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default="DIN")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    objects = models.Manager()
    published = PublishedManager()
    is_premium = models.BooleanField(default=False)
    
    def get_bookmarked_images(self):
        return self.images.all()
    
    @property
    def average_rating(self):
        ratings = self.ratings.aggregate(Avg('value'))
        return ratings['value__avg']
    
    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish']),]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('recipe:report_detail',args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug])
    tags = TaggableManager()
        
class Comment(models.Model):
    post = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]
        
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    
class Rating(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()  # Rating value, e.g., 1-5



class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def is_active(self):
        return self.end_date >= timezone.now()
    
class RecipeBook(models.Model):
    title = models.CharField(max_length=200)
    reports = models.ManyToManyField(Report, related_name='recipe_books')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title