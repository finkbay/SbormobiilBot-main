from django import forms

from .models import Profile
from .models import Timetable
from .models import UserReport


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'name',
            'amount'
        )
        widgets = {
            'name': forms.TextInput,
            'amount': forms.TextInput,

        }


class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = (
            'date',
            'street'
        )
        widgets = {
            'date': forms.DateTimeInput,
            'street': forms.TextInput,
        }


class UserReportForm(forms.ModelForm):
    class Meta:
        model = UserReport
        fields = (
            'user_id',
            'material',
            'amount'
        )
        widgets = {
            'user_id': forms.TextInput,
            'name': forms.TextInput,
            'amount': forms.TextInput,

        }
