from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Testimonial
from django.contrib.auth import get_user_model

User = get_user_model()


# Signup Form
class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(label='Profile Picture', required=False)
    confirmation_token = forms.CharField(widget=forms.HiddenInput(), required=False)  # Add this field

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2', 'profile_picture')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
    
# LOGIN
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

#USER MODEL
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')


#password reset
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email')




# feed back form
from django import forms
from .models import Testimonial

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['feedback']
        labels = {
            'feedback': 'Share Your Success Story:'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TestimonialForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user_name'] = forms.CharField(
                label='Your Name:',
                initial=user.username,
                disabled=True
            )
            self.fields['user_email'] = forms.EmailField(
                label='Your Email:',
                initial=user.email,
                disabled=True
            )



