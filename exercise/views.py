from .forms import TestimonialForm
from .models import Testimonial
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import SignupForm, LoginForm
from django.contrib.auth import get_user_model

User = get_user_model()

# SIGNUP
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            send_confirmation_email(request, user)  # Send confirmation email
            messages.success(request, 'Please check your email to confirm your account.')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def send_confirmation_email(request, user):
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    confirmation_link = request.build_absolute_uri(reverse('confirm_email', kwargs={'uidb64': uidb64, 'token': token}))
    subject = 'Confirm your email address'
    message = f"Please click the following link to confirm your email address: {confirmation_link}"
    send_mail(subject, message, 'enote7y@gmail.com', [user.email])


from django.contrib import messages  # Make sure to import messages
 
# LOGIN
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.email_confirmed:
                    login(request, user)
                    return redirect('home')
                else:
                    form.add_error(None, 'Please confirm your email address to log in.')
            else:
                # Pass error message to the form
                form.add_error(None, 'Invalid email or password. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# EMAIL CONFIRMATION
def confirm_email(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64), 'utf-8')
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.email_confirmed = True
        user.save()
        return render(request, 'email_confirmed.html')
    else:
        return render(request, 'email_confirmation_invalid.html')

def email_confirmation(request):
    return render(request, 'confirmation_email.html')

def email_confirmed(request):
    return render(request, 'email_confirmed.html')

def email_confirmation_invalid(request):
    return render(request, 'email_confirmation_invalid.html')

# PASSWORD RESET
def send_password_reset_email(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, 'User with this email does not exist.')
        return None

    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
    email_subject = 'Password Reset'
    email_body = render_to_string('password_reset_email.html', {'reset_url': reset_url})
    send_mail(email_subject, email_body, 'enote7y@gmail.com', [email])



@login_required  # Ensure that the user is logged in to submit testimonials
def home(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)  # Create but don't save yet
            testimonial.user_id = request.user.id  # Set the user_id
            testimonial.save()  # Now save the testimonial with the user_id
            return redirect('home')  # Redirect to the Home page after successful form submission
    else:
        form = TestimonialForm()
    
    testimonials = Testimonial.objects.all()  # Retrieve all testimonials
    context = {
        'form': form,
        'testimonials': testimonials,
    }
    return render(request, 'home.html', context)


def index (request):
    return render(request, 'index.html')




def csrf_failure_view(request, reason=""):
    return render(request, 'csrf_failure.html', {'reason': reason})







@login_required
def fitness_programs(request):
    programs = [
        {
            'title': 'Strength Training',
            'description': 'Build muscle and improve strength with our intensive strength training program.',
            'duration': '8 weeks',
            'price': '$149.99',
            'video_src': 'strength_training.mp4',
            'image_src': 'images/d.jpg',
        },
        {
            'title': 'Cardio Blast',
            'description': 'Get your heart pumping and burn calories with our high-intensity cardio blast program.',
            'duration': '6 weeks',
            'price': '$129.99',
            'video_src': 'cardio_blast.mp4',
            'image_src': 'images/b.jpg',
        },
        {
            'title': 'Yoga for Relaxation',
            'description': 'Unwind and improve flexibility with our calming yoga for relaxation program.',
            'duration': '4 weeks',
            'price': '$99.99',
            'video_src': 'a.mp4',
            'image_src': 'images/a.jpg',
        },
    ]

    context = {
        'programs': programs,
    }
    return render(request, 'fitness_programs.html', context)


@login_required
def display_videos(request):
    return render(request, 'videos.html')



@login_required
def contact_us(request):
    contacts = [
        {
            'name': 'Namatovu Irene',
            'image': 'images/namatovu_irene.jpg',
            'email': 'namatovu.irene@example.com',
            'phone': '+1 234 567 890',
        },
        {
            'name': 'Barigye Ronald',
            'image': 'images/barigye_ronald.jpg',
            'email': 'barigye.ronald@example.com',
            'phone': '+1 345 678 901',
        },
        {
            'name': 'Lusiba Talib',
            'image': 'images/lusiba_talib.jpg',
            'email': 'lusiba.talib@example.com',
            'phone': '+1 456 789 012',
        },
        {
            'name': 'Okidi John Bosco',
            'image': 'images/okidi_john_bosco.jpg',
            'email': 'okidi.john@example.com',
            'phone': '+1 567 890 123',
        },
        {
            'name': 'Nkajja Shafic',
            'image': 'images/nkajja_shafic.jpg',
            'email': 'nkajja.shafic@example.com',
            'phone': '+1 678 901 234',
        },
    ]
    return render(request, 'contact_us.html', {'contacts': contacts})
