from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, PasswordChangeForm
from .models import User
import magic
from django.core.exceptions import ValidationError

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class UserInfoForm(ModelForm):
  class Meta:
     model = User
     fields = ['name', 'profile_bio', 'date_of_birth', 'gender', 'blood_group', 'department','current_address', 'permanent_address',  'job_type', 'job_role', 'job_description', 'avatar', 'resume']


     def clean_avatar(self):
        file = self.cleaned_data.get('avatar')
        if file:
            mime = magic.from_buffer(file.read(2048), mime=True)
            file.seek(0)  # reset pointer so file can still be saved later

            allowed_mimes = ['image/jpeg', 'image/png']
            if mime not in allowed_mimes:
                raise ValidationError("Only .jpg, .jpeg, or .png images are allowed.")
        return file

     def clean_resume(self):
        file = self.cleaned_data.get('resume')
        if file:
            mime = magic.from_buffer(file.read(2048), mime=True)
            file.seek(0)

            allowed_mimes = ['image/jpeg', 'image/png', 'application/pdf']
            if mime not in allowed_mimes:
                raise ValidationError("Resume must be .jpg, .jpeg, .png, or .pdf.")
        return file

  
class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput())
    registrationKey = forms.CharField()


class CustomPasswordResetForm(PasswordResetForm):
  email = forms.EmailField(widget=forms.EmailInput(attrs={
      'placeholder': 'Enter your email',
      'class': 'my-input'
}))

# class UserInfoForm(ModelForm):
#   name = forms.CharField(required=True, strip=True)
#   profile_bio = forms.CharField(required=True, strip=True)
#   date_of_birth = forms.CharField(required=True, strip=True)
#   gender = forms.CharField(required=True, strip=True)
#   blood_group = forms.CharField(required=True, strip=True)
#   current_address = forms.CharField(required=False, strip=True)
#   permanent_address = forms.CharField(required=False, strip=True)
#   job_type = forms.CharField(required=False, strip=True)
#   job_role = forms.CharField(required=False, strip=True)
#   job_description = forms.CharField(required=False, strip=True)
#   class Meta:
#      model = User
#      fields = ['name', 'profile_bio', 'date_of_birth', 'gender', 'blood_group','current_address', 'permanent_address',  'job_type', 'job_role', 'job_description', 'avatar', 'resume']

  