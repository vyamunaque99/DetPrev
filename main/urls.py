from django.contrib import admin
from django.urls import path
  
# importing views from views..py
from .views import *
  
urlpatterns = [
    path('login/',login_view),
    path('register/',register_view),
    path('logout/',logout_view),
    path('dataset_generation/',dataset_generation_view),
    path('process_generation/',process_generation_view),
    path('process_generation/<str:username>/<str:dataset_name>/',process_generation_detail),
    path('assets/<str:username>/<str:dataset_name>/<str:process>/',process_view),
    path('dataset_delete/<str:username>/<str:dataset_name>/',dataset_delete),
    path('process_monitoring/',process_monitoring_view),
    path('process_monitoring_list/',process_monitoring_list_view),
    path('',main_view)
]
