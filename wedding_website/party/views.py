from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.template import loader
from .forms import GuestInfoForm, EmailValidationForm, RsvpForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import GuestUser
from .decorators import require_validation
import time
from decouple import config
import datetime

User = get_user_model()


# Home page function
def home(request):
    template = loader.get_template("party/home.html")
    context = {}

    return HttpResponse(template.render(context, request))

def guest_information(request):
    if request.method == "POST":
        form = GuestInfoForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            code = form.cleaned_data['code']
            phone_number = form.cleaned_data['phone_number']

            # Check for existing submission
            if GuestUser.objects.filter(email=email).exists() or GuestUser.objects.filter(phone_number=phone_number).exists():
                messages.error(request, "You've already submitted your information.")
                return redirect('/home')
            
            if code == config('WEBSITE_PASSWORD'):
                GuestUser.objects.create(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                email = email,
                phone_number = phone_number,
                knows = form.cleaned_data['knows'],
                is_validated = True,
                code = form.cleaned_data['code']
                )

                messages.success(request, "Welcome. Please log in")
                return redirect('/home')
            else:
                messages.error(request, "Do we know you? Do you have the password?")
        
        else:
            print(form.errors)
            messages.error(request, "Something went wrong")

    else:
        form = GuestInfoForm()
    
    return render(request, 'party/guest_info.html', {'form': form})

def validation(request):
    if request.user.is_authenticated:
        last_validated = request.session.get("last_validated", None)

        if last_validated and time.time() - last_validated <= 3600:
            # Session still valid
            return redirect('/home')
        else:
            # Session expired — log out to force re-validation
            force_logout(request)

    if request.method == 'POST':
        email = request.POST.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            user = User.objects.get(email=email)

            if user.is_validated:
                request.session["last_validated"] = time.time()
                auth_login(request, user)
                request.session.set_expiry(0)  # Session expires on browser close
                return redirect("/home")
            else:
                messages.error(request, "Your email has not been validated yet.")
                return redirect("/validation")

        else:
            messages.error(request, "Do we know you?")
            return redirect("/validation")

    form = EmailValidationForm()
    return render(request, 'party/email_validation.html', {'form': form})

def force_logout(request):
    logout(request)
    request.session.flush()
    print("✅ User logged out")
    messages.warning(request, "Session expired. Please validate again.")
    return redirect('/home/')

def check_session(request):
    # print("⚠️ check_session was hit! User authenticated:", request.user.is_authenticated)
    return JsonResponse({'session_active': request.user.is_authenticated})

# Not needed
# # Cannot see story page unless email has been verified
@require_validation
def story_protected(request):    
     template = loader.get_template("party/story.html")
     context = {}
     return HttpResponse(template.render(context, request))

# Cannot see rsvp page unless email has been verified
@require_validation
def rsvp_protected(request):
    if request.user.invitation.exists():
        return render(request, 'party/already_submitted.html')  # Prevent duplicate
    
    current_date = datetime.date.today()
    if current_date > datetime.date(2025, 8, 10):
        return render(request, 'party/rsvp_closed.html')
    
    if request.method == 'POST':
        form = RsvpForm(request.POST)
        if form.is_valid():
            email = request.user.email
            name = form.cleaned_data.get("name")
            attend = form.cleaned_data.get("attend")
            group_type = form.cleaned_data.get("group_type")
            number_of_guests = form.cleaned_data.get("guest_count")
            guest_names = form.cleaned_data.get('guest_names')
            invite = form.cleaned_data.get("invite")
            
            user_email = GuestUser.objects.get(email=email)

            invitation = form.save(commit=False)
            invitation.email = user_email
            invitation.save()

            messages.success(request, 'Record has been submitted')
            return render(request, "party/success.html")
        
    else:
        initial_data = {}
        if request.user.is_authenticated:
            full_name = f"{request.user.first_name} {request.user.last_name}"
            initial_data['name'] = full_name.strip()
        form = RsvpForm(initial=initial_data)
    
    return render(request, 'party/rsvp_protected.html', {'form': form})


# Cannot see schedule page unless email has been verified
@require_validation
def schedule_protected(request):
    template = loader.get_template("party/schedule_protected.html")
    context = {}
    return HttpResponse(template.render(context, request))

@require_validation
def travel(request):
    template = loader.get_template("party/travel.html")
    context = {}
    return HttpResponse(template.render(context, request))

@require_validation
def party_protected(request):    
     template = loader.get_template("party/wedding_party.html")
     context = {}
     return HttpResponse(template.render(context, request))


def faq(request):
    template = loader.get_template("party/faq.html")
    context = {}
    return HttpResponse(template.render(context, request))


@login_required
def your_form_view(request):
    if not request.user.is_authenticated:
        return redirect('/validation/')  # Redirect if session expired
