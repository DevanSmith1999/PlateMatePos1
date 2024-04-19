from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm  # Import your SignupForm from forms.py



@login_required
def home(request):
 return render(request, "PlateMate/home.html", {})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            if User.objects.filter(username=username).exists():
                error_message = "Username is already taken."
                return render(request, 'signup.html', {'form': form, 'error_message': error_message})
            elif User.objects.filter(email=email).exists():
                error_message = "Email address is already registered."
                return render(request, 'signup.html', {'form': form, 'error_message': error_message})
            else:
                form.save()
                return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})