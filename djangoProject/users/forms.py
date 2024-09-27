from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from teams.models import Team, Subteam
from django.core.exceptions import ValidationError
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=True,
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    subteam = forms.ModelChoiceField(queryset=Subteam.objects.all(), required=True,
                                     widget=forms.Select(attrs={'class': 'form-select'}))
    college_id = forms.CharField(max_length=9, min_length=9, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    new_member = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number', 'team', 'subteam', 'college_id', 'new_member')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        # Ensure consistent styling for form fields
        for field_name, field in self.fields.items():
            if field_name != 'new_member':
                field.widget.attrs.update({'class': 'form-control'})

    def clean_college_id(self):
        college_id = self.cleaned_data.get('college_id')
        if Profile.objects.filter(college_id=college_id).exists():
            raise ValidationError('A profile with this college ID already exists.')
        return college_id

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if Profile.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('A profile with this phone number already exists.')
        return phone_number
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = None

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        return password1


class UserUpdateForm(forms.ModelForm):
    college_id = forms.CharField(max_length=9, min_length=9, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    new_member = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        if hasattr(self.instance, 'profile'):
            self.fields['college_id'].initial = self.instance.profile.college_id
            self.fields['phone_number'].initial = self.instance.profile.phone_number
            self.fields['new_member'].initial = self.instance.profile.new_member

        for field_name, field in self.fields.items():
            if field_name != 'new_member':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'

    def clean_college_id(self):
        college_id = self.cleaned_data.get('college_id')
        if Profile.objects.filter(college_id=college_id).exclude(user=self.instance).exists():
            raise ValidationError('A profile with this college ID already exists.')
        return college_id

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if Profile.objects.filter(phone_number=phone_number).exclude(user=self.instance).exists():
            raise ValidationError('A profile with this phone number already exists.')
        return phone_number