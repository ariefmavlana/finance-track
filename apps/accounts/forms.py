from django import forms
from .models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "avatar", "timezone", "base_currency"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "first_name": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "last_name": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "timezone": forms.Select(attrs={"class": "select select-bordered w-full"}, choices=[
                ("Asia/Jakarta", "Asia/Jakarta"),
                ("UTC", "UTC"),
                ("America/New_York", "America/New_York"),
                ("Europe/London", "Europe/London"),
            ]),
            "base_currency": forms.Select(attrs={"class": "select select-bordered w-full"}, 
                choices=[
                ("IDR", "IDR"),
                ("USD", "USD"),
                ("EUR", "EUR"),
                ("SGD", "SGD"),
                ("JPY", "JPY"),           
                ],
            ),
        }