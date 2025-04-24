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
    path("info_form/", views.guest_information, name ='guest information'),
    path("travel/", views.travel, name = "accommodations"),
    path("faq/", views.faq, name = "FAQ"),
    path('check-session/', views.check_session, name='check_session'),
    path("force-logout/", views.force_logout, name="force_logout"),
]

urlpatterns += staticfiles_urlpatterns()