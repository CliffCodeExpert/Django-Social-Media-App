from django import forms
from .models import Profile, Post

class ProfileForm(forms.ModelForm):
    profileimg = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={"class": "profileimg"}),
        label="Profile Image",
    )
    location = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Your Location", "class": "location"}),
        label="Location",
    )
    bio = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Your Bio", "class": "bio"}),
        label="Bio",
        max_length=100, 
    )

    class Meta:
        model = Profile
        fields = ['profileimg', 'location', 'bio']

class PostForm(forms.ModelForm):
    image = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={"class": "postimg"}),
        label="Image",
    )
    caption = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Write a caption..."}),
        label="Caption",
        max_length=100,  
    )

    class Meta:
        model = Post
        exclude = ('user', 'id', 'created_at', 'no_of_likes')
