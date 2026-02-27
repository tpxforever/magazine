from django import forms
from .models import Article, UserProfile


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title', 'article_type', 'category', 'subject_title',
            'subject_year', 'director', 'rating', 'excerpt',
            'body', 'cover_image', 'cover_image_url',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Your article title...'}),
            'subject_title': forms.TextInput(attrs={'placeholder': 'e.g. Oppenheimer'}),
            'subject_year': forms.TextInput(attrs={'placeholder': 'e.g. 2023'}),
            'director': forms.TextInput(attrs={'placeholder': 'e.g. Christopher Nolan'}),
            'excerpt': forms.Textarea(attrs={'rows': 3, 'placeholder': 'A compelling 1-2 sentence summary...'}),
            'body': forms.Textarea(attrs={'rows': 20, 'placeholder': 'Write your piece here...'}),
            'cover_image_url': forms.URLInput(attrs={'placeholder': 'https://...'}),
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 10, 'step': 0.5}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 0 or rating > 10):
            raise forms.ValidationError('Rating must be between 0 and 10.')
        return rating


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = ['bio', 'year_of_study', 'university', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user_id:
            user = self.instance.user
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile
