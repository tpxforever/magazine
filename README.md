# CinemaWords — Student Film & TV Magazine

A Django-powered student magazine for film and television criticism.

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run migrations

```bash
python manage.py migrate
```

### 3. Create a superuser (for the admin panel)

```bash
python manage.py createsuperuser
```

### 4. (Optional) Seed some sample categories

```bash
python manage.py shell
```

Then in the shell:

```python
from articles.models import Category
Category.objects.create(name="Drama", slug="drama", media_type="both")
Category.objects.create(name="Horror", slug="horror", media_type="film")
Category.objects.create(name="Comedy", slug="comedy", media_type="both")
Category.objects.create(name="Streaming", slug="streaming", media_type="tv")
Category.objects.create(name="Documentary", slug="documentary", media_type="film")
exit()
```

### 5. Run the dev server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

Admin panel: http://127.0.0.1:8000/admin

---

## Project Structure

```
cinemawords/
├── cinemawords/          # Project config (settings, urls, wsgi)
├── articles/             # Main app
│   ├── models.py         # Article, Category, UserProfile
│   ├── views.py          # All views
│   ├── forms.py          # ArticleForm, UserProfileForm
│   ├── admin.py          # Admin with publish/reject actions
│   └── urls.py           # URL routing
├── templates/
│   ├── base.html         # Base layout with nav + footer
│   ├── articles/         # All page templates
│   └── registration/     # Auth templates
├── static/
│   ├── css/main.css      # Full design system
│   └── js/main.js        # Animations + interactions
└── manage.py
```

---

## Customisation Tips

### Branding
- Change "CinemaWords" → search for it in `base.html` and `main.css`
- Update colors in `:root` in `main.css` — `--gold`, `--card`, `--black` etc.
- Swap Google Fonts in `base.html` `<head>`

### Admin Workflow
Articles submitted by users land as `pending`. In the Django admin:
- Go to **Articles > Articles**
- Select submissions and use the **"Publish selected articles"** action
- Or change status and tick **featured** for the homepage hero

### Adding Features
- **Tags/genres**: Add a ManyToMany `tags` field to `Article`
- **Comments**: Add a `Comment` model FK to `Article`
- **Newsletter**: Integrate Mailchimp or Django's email backend
- **Rich text editor**: Drop in `django-ckeditor` or `django-prose-editor`

---

## Design System

Dark editorial aesthetic with:
- **Playfair Display** (display/headlines) + **DM Sans** (body) + **DM Mono** (labels/meta)
- Gold (`#c9a84c`) accent throughout
- Scroll-triggered reveal animations (`.reveal` class)
- Custom gold cursor dot on desktop
- Responsive — mobile nav collapses to burger menu
