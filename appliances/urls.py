from django.urls import path

from appliances import views

urlpatterns = [
    path('homeowner/appliances/', views.list_appliances, name='list_appliances'),
    path('homeowner/appliances/add/', views.add_appliance, name='add_appliance'),
    path('homeowner/appliances/<int:pk>/edit/', views.edit_appliance, name='edit_appliance'),
    path('homeowner/appliances/<int:pk>/delete/', views.delete_appliance, name='delete_appliance'),
    path('homeowner/appliances/<int:pk>/toggle/', views.toggle_appliance, name='toggle_appliance'),
    path('homeowner/appliances/<int:pk>/fault/', views.report_fault, name='report_fault'),
]
