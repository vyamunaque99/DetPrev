from django.contrib import admin
from django.urls import path
  
# importing views from views..py
from .views import *
  
urlpatterns = [
    path('login/',login_view),
    path('register/',register_view),
    path('logout/',logout_view),
    path('dataset_generation/',dataset_generation_view),
    path('',main_view)
]
