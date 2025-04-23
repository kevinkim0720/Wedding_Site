from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.template import loader
from .forms import GuestInfoForm, EmailValidationForm, RsvpForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import guestuser
from .decorators import require_validation
import time

User = get_user_model()


# Home page function
def home(request):
    template = loader.get_template("party/home.html")
    context = {}

    return HttpResponse(template.render(context, request))

def validation(request):
    if request.user.is_authenticated:
        # If the user is already logged in, check if validation expired
        last_validated = request.session.get("last_validated", None)
        if last_validated and time.time() - last_validated <= 3600:  # 1 hour
            return redirect('/home')  # If within 1 hour, go to home
        
        # If validation expired, logout and force revalidation
        logout(request)
        messages.warning(request, "Session expired. Please validate again.")
        return redirect('/validation')

    
    if request.method == 'POST':
        email = request.POST.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            user = User.objects.get(email = email)

            if user.is_validated:
                request.session["last_validated"] = time.time()
                auth_login(request, user)
                return redirect("/home")
            else:
                messages.error(request, "Your email has not been validated yet.")
                return redirect("/validation")

        else:
            messages.error(request, "Do we know you?")
            return redirect("/validation")

    form = EmailValidationForm()
    return render(request, 'party/email_validation.html', {'form': form})

def guest_information(request):
    if request.method == "POST":
        form = GuestInfoForm(request.POST)

        if form.is_valid():
            guestuser.objects.create(
            first_name = form.cleaned_data['first_name'],
            last_name = form.cleaned_data['last_name'],
            email = form.cleaned_data['email'],
            phone_number = form.cleaned_data['phone_number'],
            knows = form.cleaned_data['knows']
            )

            messages.success(request, "Please wait a day to be verfied")
            return redirect('/home')
        
        else:
            print(form.errors)
            messages.error(request, "Something went wrong")

    else:
        form = GuestInfoForm()
    
    return render(request, 'party/guest_info.html', {'form': form})

# Cannot see story page unless email has been verified
@require_validation
def story_protected(request):
    template = loader.get_template("party/story.html")
    context = {}
    return HttpResponse(template.render(context, request))

# Cannot see rsvp page unless email has been verified
@require_validation
def rsvp_protected(request):
    if request.method == 'POST':
        form = RsvpForm(request.POST)
        if form.is_valid():
            email = request.user.email
            invite = form.cleaned_data.get("invitation")
            address = form.cleaned_data.get("address")
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            zip_code = form.cleaned_data.get('zip_code')
            group_type = form.cleaned_data.get("group_type")
            number_of_guests = form.cleaned_data.get("guest_count")
            guest_names = form.cleaned_data.get('guest_names')
            
            user_email = guestuser.objects.get(email=email)

            invitation = form.save(commit=False)
            invitation.email = user_email
            invitation.save()

            messages.success(request, 'Record has been submitted')
            return render(request, "party/success.html")
        
    else:
        form = RsvpForm()
    
    return render(request, 'party/rsvp_protected.html', {'form': form})

# Cannot see schedule page unless email has been verified
@require_validation
def schedule_protected(request):
    template = loader.get_template("party/schedule_protected.html")
    context = {}
    return HttpResponse(template.render(context, request))

def travel(request):
    template = loader.get_template("party/travel.html")
    context = {}
    return HttpResponse(template.render(context, request))

def faq(request):
    template = loader.get_template("party/faq.html")
    context = {}
    return HttpResponse(template.render(context, request))

def check_session(request):
    if request.user.is_authenticated:
        return JsonResponse({'session_active': True})
    else:
        return JsonResponse({'session_active': False})

@login_required
def your_form_view(request):
    if not request.user.is_authenticated:
        return redirect('/validation/')  # Redirect if session expired