from django.urls import path

from pricing import views

urlpatterns = [
    path('homeowner/pricing/', views.pricing_plan_page, name='pricing_plan_page'),
]
