import datetime

from django import forms
from django.forms import ModelForm, DateInput
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from catalog.models import BookInstance


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        widget=DateInput(attrs={"type": "date"}),
        help_text="Enter a date between now and 4 weeks (default 3).",
    )

    def clean_renewal_date(self):
        data = self.cleaned_data["renewal_date"]

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_("Invalid date - renewal in past"))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid date - renewal more than 4 weeks ahead"))

        # Remember to always return the cleaned data.
        return data


# using models forms
# class RenewBookModelForm(ModelForm):
#     def clean_due_back(self):
#         data = self.cleaned_data["due_back"]

#         # Check if a date is not in the past.
#         if data < datetime.date.today():
#             raise ValidationError(_("Invalid date - renewal in past"))

#         # Check if a date is in the allowed range (+4 weeks from today).
#         if data > datetime.date.today() + datetime.timedelta(weeks=4):
#             raise ValidationError(_("Invalid date - renewal more than 4 weeks ahead"))

#         # Remember to always return the cleaned data.
#         return data

#     class Meta:
#         model = BookInstance
#         fields = ["due_back"]
#         labels = {"due_back": _("Renewal date")}
#         help_texts = {
#             "due_back": _("Enter a date between now and 4 weeks (default 3).")
#         }


class CreateBookInstanceForm(ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data["due_back"]

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_("Invalid date - due date in past"))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid date - due date more than 4 weeks ahead"))

        # Remember to always return the cleaned data.
        return data

    class Meta:
        model = BookInstance
        fields = ["imprint", "due_back"]
        labels = {
                "due_back": _("Renewal date"),
                "imprint": _("Imprint"),
            },
        
        help_texts = {
            "due_back": _(
                "Enter a date between now and 4 weeks to return the borrowed book."
            ),
            "imprint": _("Enter the publisher or edition of the book you want to borrow."),
        }
        
        widgets = {
            "status": forms.HiddenInput(attrs={"value": "o"}),
            'due_back': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'imprint': forms.TextInput(attrs={'class': 'form-control'}),
        }
        

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("Sorry, this email address is not valid. Please try again.")
        return email


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please choose a different email")
        return email
        
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
