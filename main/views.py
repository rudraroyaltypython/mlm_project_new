from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
from main.models import UserProfile
from django.contrib import messages
from .forms import LoginForm  # Assuming you're using a form to handle login
from django.contrib.auth import logout

def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def products(request):
    return render(request, 'main/products.html') 

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Handle additional fields
            full_name = form.cleaned_data['full_name']
            contact_number = form.cleaned_data['contact_number']
            payment_upi = form.cleaned_data.get('payment_upi')
            pancard_image = request.FILES.get('pancard_image')

            # Save PAN card image
            if pancard_image:
                fs = FileSystemStorage()
                fs.save(pancard_image.name, pancard_image)

            # Redirect to login after successful registration
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})

# Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Retrieve the user from the form
            user = form.get_user()
            # Log the user in by passing both request and user
            login(request, user)  # Correctly calling the login function
            return redirect('dashboard')  # Redirect to home after successful login
        else:
            return render(request, 'main/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    # Fetch user-specific data
    business_growth = user_profile.business_growth
    earnings = user_profile.earnings
    referrals = user_profile.referrals
    achievements = user_profile.achievements.split(',') if user_profile.achievements else []
    target = user_profile.target
    current_progress = (business_growth / target) * 100  # Calculate target progress

    context = {
        'business_growth': business_growth,
        'earnings': earnings,
        'referrals': referrals,
        'achievements': achievements,
        'target': target,
        'current_progress': current_progress,
    }
    return render(request, 'main/dashboard.html', context)


def export_users_csv(request):
    # Fetch all user profiles
    user_profiles = UserProfile.objects.all()
    
    # Prepare CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_profiles.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Business Growth', 'Earnings', 'Referrals', 'Is Retired'])  # Header row

    for profile in user_profiles:
        writer.writerow([profile.user.username, profile.business_growth, profile.earnings, profile.referrals, profile.is_retired])

    return response

@login_required
def retire_user(request):
    user_profile = request.user.userprofile
    target = user_profile.target

    if user_profile.business_growth >= target:
        user_profile.is_retired = True
        user_profile.save()
        # Optionally send a notification or email to the user
        return redirect('home')  # Redirect to homepage after retirement
    else:
        return render(request, 'main/retirement_failed.html')  # Show a message if the target is not met

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user if authenticated
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard after successful login
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')  # Redirect to the login page if authentication fails

    return render(request, 'registration/login.html')  # If GET request, render the login form  


def custom_logout(request):
    logout(request)
    return redirect('home')