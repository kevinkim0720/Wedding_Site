from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("home/", views.home, name = 'home'),
    path("", views.home, name = "home"),
    path("validation/", views.validation, name ="validated email"),
    path("kamy/", views.story_protected, name = "story"),
    path("info/", views.schedule_protected, name = 'schedule'),
    path("rsvp/", views.rsvp_protected, name = 'rsvp'),
    path("info_form/", views.guest_information, name ='guest information')
]

urlpatterns += staticfiles_urlpatterns()