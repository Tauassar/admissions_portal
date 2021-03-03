from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboardView, name='dashboard'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('info/', views.infoView, name='info'),
    path('contacts/', views.contactsView, name='contacts'),
    path('personal/', views.personalView, name='personal'),
    path('chair/', views.ChairView, name='chair'),
    path('profile/<str:uuid>/', views.profileView, name='profile'),
    path('candidate_evaluate/<str:uuid>/', views.candidateEvaluateView, name='candidate_evaluate'),
    path('create_candidate/', views.createCandidateView, name='create_candidate'),
    path('observe_candidate/<str:candidate_id>/', views.createCandidateView, name='observe_candidate'),
    path('approve_evaluation/<str:uuid>/', views.approveEvalView, name='approve_evaluation'),
]
