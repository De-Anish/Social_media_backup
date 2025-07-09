from django import forms
from .models import Tweet, UserProfile

class tweetform(forms.ModelForm):
    class Meta: 
        model = Tweet
        fields = ['text', 'photo']
        widgets = {
            'text': forms.Textarea(attrs={
                'id': 'id_text',
                'class': 'text-input',
                'placeholder': "What's on your mind?",
                'maxlength': '240',
                'required': 'required'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'id': 'id_photo',
                'class': 'file-input',
                'accept': 'image/*'
            }),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_photo']