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
    path('secretary/', views.SecretaryView, name='secretary'),
    path('profile/<str:uuid>/', views.profileView, name='profile'),
    path('candidate_evaluate/<str:uuid>/', views.candidateEvaluateView, name='candidate_evaluate'),
    path('create_candidate/', views.createCandidateView, name='create_candidate'),
    path('observe_candidate/<str:candidate_id>/',   \
         views.createCandidateView, name='observe_candidate'),
    path('approve_evaluation/<str:uuid>/', views.approveEvalView, name='approve_evaluation'),
    path('candidates/', views.CandidatesList.as_view()),
    path('candidates/<str:candidate_id>/', views.CandidateDetail.as_view()),
    path('excell_application/<str:evaluation_id>/', views.GetApplicationEvaluationAsExcellView, name='excell_application'),
    path('excell_interview/<str:evaluation_id>/', views.GetInterviewEvaluationAsExcellView, name='excell_interview')
]
