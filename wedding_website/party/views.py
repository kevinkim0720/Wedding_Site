from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.template import loader
from .forms import GuestInfoForm, EmailValidationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages

# Home page function
def home(request):
    template = loader.get_template("party/home.html")
    context = {}
    return HttpResponse(template.render(context, request))

def validation(request):
    if request.user.is_authenticated:
        return redirect('/home')
    
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email__iexact=email).exists():
            user = authenticate(request, email = email)

            if user is not None:
                auth_login(request, user)
                return redirect("/home")
            
        else:
            messages.error(request, "Do we know you?")
            return redirect("/validation")
    else:
        form = EmailValidationForm()
    
    return render(request, 'party/email_validation.html', {'form': form})

def guest_information(request):
    if request.method == "POST":
        form = GuestInfoForm()
        if form.is_valid():
            first = form.cleaned_data['first_name']
            last = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            number = form.cleaned_data['phone_number']
            know = form.cleaned_data['knows']
    else:
        form = GuestInfoForm()
    
    return render(request, 'party/guest_info.html', {'form': form})

# Cannot see story page unless email has been verified
def story_protected(request):
    template = loader.get_template("party/story.html")
    context = {}
    return HttpResponse(template.render(context, request))

# Cannot see rsvp page unless email has been verified
def rsvp_protected(request):
    if request.method == 'POST':
        form = EmailValidationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email__iexact=email).exists():
                return render(request, 'party/rsvp.html')
    else:
        form = EmailValidationForm()
    
    return render(request, 'party/email_validation.html', {'form': form})

# Cannot see schedule page unless email has been verified
def schedule_protected(request):
    template = loader.get_template("party/schedule.html")
    context = {}
    return HttpResponse(template.render(context, request))