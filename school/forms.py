from django import forms
from datetime import datetime
from .models import UserBase
from django.utils.crypto import get_random_string

class AdmitMemberForm(forms.ModelForm):
    class Meta:
        model = UserBase
        fields = ['user_type', 'full_name', 'email', 'phone', 'dob']

    user_type = forms.ChoiceField(choices=UserBase.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    def save(self, commit=True):
        instance = super().save(commit=False)

        # 1. Prefix based on user_type
        prefix_map = {
            'student': 'STD',
            'teacher': 'EMP',
            'school': 'SCH'
        }

        prefix = prefix_map.get(instance.user_type.lower(), 'USR')

        # 2. Get current year’s last two digits
        year_suffix = str(datetime.now().year)[-2:]

        # 3. Get last serial number for this user_type in current year
        existing_users = UserBase.objects.filter(user_type=instance.user_type, user_id__startswith=prefix + year_suffix).order_by('-user_id')
        if existing_users.exists():
            last_id = existing_users.first().user_id
            last_serial = int(last_id[-5:])  # last 5 digits
            new_serial = str(last_serial + 1).zfill(5)
        else:
            new_serial = '00001'

        # 4. Final ID
        instance.user_id = f"{prefix}{year_suffix}{new_serial}"

        # 5. Set password (phone as default)
        instance.set_password(instance.phone)

        if commit:
            instance.save()
        return instance


class LoginForm(forms.Form):
    user_id = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your ID or email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))


# Change password form for first-time login
class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        new = cleaned_data.get("new_password")
        confirm = cleaned_data.get("confirm_password")
        if new != confirm:
            raise forms.ValidationError("Passwords do not match.")
