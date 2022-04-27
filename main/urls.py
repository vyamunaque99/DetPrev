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
    path('stakeholder/',stakeholder_view),
    path('stakeholder/create_or_update/',stakeholder_create_or_update),
    path('stakeholder/create_or_update/<int:stakeholder_id>/',stakeholder_create_or_update),
    path('stakeholder/delete/<int:stakeholder_id>/',stakeholder_delete),
    path('stakeholder_list/',stakeholder_list_view),
    path('stakeholder_list/create_or_update/',stakeholder_list_create_or_update),
    path('stakeholder_list/create_or_update/<int:stakeholder_list_id>/',stakeholder_list_create_or_update),
    path('stakeholder_list/delete/<int:stakeholder_list_id>/',stakeholder_list_create_or_update),
    path('stakeholder_list_detail/',stakeholder_list_detail_view),
    path('stakeholder_list_detail/create_or_update/',stakeholder_list_detail_create_or_update),
    path('stakeholder_list_detail/create_or_update/<int:stakeholder_list_id>/',stakeholder_list_detail_create_or_update),
    path('stakeholder_list_detail/delete/<int:stakeholder_list_id>/',stakeholder_list_detail_create_or_update),
    path('',main_view)
]
