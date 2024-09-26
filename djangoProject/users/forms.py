from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from teams.models import Team, Subteam

class CustomUserCreationForm(UserCreationForm):
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=True,
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    subteam = forms.ModelChoiceField(queryset=Subteam.objects.all(), required=True,
                                     widget=forms.Select(attrs={'class': 'form-select'}))
    college_id = forms.CharField(max_length=9, min_length=9, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    new_member = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number', 'team', 'subteam', 'college_id', 'new_member')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        # Ensure consistent styling for form fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = None

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        return password1


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
