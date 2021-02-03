from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('info/', views.infoView, name='info'),
    path('contacts/', views.contactsView, name='contacts'),
    path('candidate/<str:uuid>/', views.candidateView, name='candidate'),
    path('personal/', views.personalView, name='personal'),
    path('', views.dashboardView, name='dashboard'),
    path('create_candidate/', views.createCandidateView, name='create_candidate'),
    path('approve_evaluation/<str:uuid>/', views.approveEvalView, name='approve_evaluation'),
]
