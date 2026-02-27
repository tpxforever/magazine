from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Article, Category, UserProfile
from .forms import ArticleForm, UserProfileForm


def home(request):
    featured = Article.objects.filter(status='published', featured=True).first()
    recent = Article.objects.filter(status='published').exclude(featured=True)[:8]
    film_articles = Article.objects.filter(
        status='published', article_type='review', category__media_type='film'
    )[:4]
    tv_articles = Article.objects.filter(
        status='published', article_type='review', category__media_type='tv'
    )[:4]
    categories = Category.objects.all()
    context = {
        'featured': featured,
        'recent': recent,
        'film_articles': film_articles,
        'tv_articles': tv_articles,
        'categories': categories,
    }
    return render(request, 'articles/home.html', context)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    article.views += 1
    article.save(update_fields=['views'])
    related = Article.objects.filter(
        status='published', article_type=article.article_type
    ).exclude(pk=article.pk)[:3]
    return render(request, 'articles/detail.html', {'article': article, 'related': related})


def article_list(request):
    articles = Article.objects.filter(status='published')
    q = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    media_type = request.GET.get('type', '')
    article_type = request.GET.get('kind', '')

    if q:
        articles = articles.filter(
            Q(title__icontains=q) | Q(body__icontains=q) |
            Q(subject_title__icontains=q) | Q(author__username__icontains=q)
        )
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
    if media_type:
        articles = articles.filter(category__media_type=media_type)
    if article_type:
        articles = articles.filter(article_type=article_type)

    categories = Category.objects.all()
    return render(request, 'articles/list.html', {
        'articles': articles,
        'categories': categories,
        'q': q,
        'selected_category': category_slug,
        'selected_type': media_type,
        'selected_kind': article_type,
    })


@login_required
def submit_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.status = 'pending'
            article.save()
            messages.success(request, 'Your piece has been submitted for review. We\'ll be in touch!')
            return redirect('dashboard')
    else:
        form = ArticleForm()
    return render(request, 'articles/submit.html', {'form': form})


@login_required
def edit_article(request, slug):
    article = get_object_or_404(Article, slug=slug, author=request.user)
    if article.status == 'published':
        messages.error(request, 'Published articles cannot be edited.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated.')
            return redirect('dashboard')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/submit.html', {'form': form, 'editing': True})


@login_required
def dashboard(request):
    user_articles = Article.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'articles/dashboard.html', {'user_articles': user_articles})


@login_required
def profile_edit(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'articles/profile_edit.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Welcome to CinemaWords, {user.username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def about(request):
    return render(request, 'articles/about.html')
