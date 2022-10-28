from django import forms
from .models import Reply, Ad


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ("content",)


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ["title", "content", "media_content", "guild"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
            "guild": forms.Select(attrs={"class": "form-control"}),
        }
