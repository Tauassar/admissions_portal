from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboardView, name='dashboard'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('info/', views.infoView, name='info'),
    path('contacts/', views.contactsView, name='contacts'),
    path('candidate_evaluate/<str:uuid>/', views.candidateEvaluateView, name='candidate_evaluate'),
    path('personal/', views.personalView, name='personal'),
    path('set_threshold/', views.setThresholdView, name='set_threshold'),
    path('profile/<str:uiid>/', views.profileView, name='profile'),
    path('create_candidate/', views.createCandidateView, name='create_candidate'),
    path('observe_candidate/<str:uuid>/', views.observeCandidateView, name='observe_candidate'),
    path('approve_evaluation/<str:uuid>/', views.approveEvalView, name='approve_evaluation'),
]
