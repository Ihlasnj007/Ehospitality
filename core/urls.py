from django.urls import path
from . import views

urlpatterns = [
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('contact/', views.contact, name='contact'),
    path('help/', views.help_center, name='help'),
]
