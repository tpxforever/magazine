from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    FILM = 'film'
    TV = 'tv'
    BOTH = 'both'
    TYPE_CHOICES = [
        (FILM, 'Film'),
        (TV, 'Television'),
        (BOTH, 'Film & TV'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    media_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=BOTH)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_PENDING = 'pending'
    STATUS_PUBLISHED = 'published'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PENDING, 'Pending Review'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    TYPE_REVIEW = 'review'
    TYPE_ESSAY = 'essay'
    TYPE_INTERVIEW = 'interview'
    TYPE_LIST = 'list'
    TYPE_CHOICES = [
        (TYPE_REVIEW, 'Review'),
        (TYPE_ESSAY, 'Essay'),
        (TYPE_INTERVIEW, 'Interview'),
        (TYPE_LIST, 'List'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    article_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_REVIEW)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    cover_image_url = models.URLField(blank=True, help_text='Or paste an image URL instead of uploading')
    excerpt = models.TextField(max_length=400, help_text='Short summary shown on listing pages')
    body = models.TextField()
    subject_title = models.CharField(max_length=255, blank=True, help_text='Name of the film/show being discussed')
    subject_year = models.CharField(max_length=10, blank=True, help_text='Release year')
    director = models.CharField(max_length=255, blank=True, help_text='Director/Creator name')
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, help_text='Rating out of 10')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

    def get_cover(self):
        if self.cover_image:
            return self.cover_image.url
        return self.cover_image_url or None


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    year_of_study = models.CharField(max_length=50, blank=True)
    university = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} profile'
