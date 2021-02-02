from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboardView, name='dashboard'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('info/', views.infoView, name='info'),
    path('contacts/', views.contactsView, name='contacts'),
    path('personal/', views.personalView, name='personal'),
]
