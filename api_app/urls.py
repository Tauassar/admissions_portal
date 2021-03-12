from django.urls import path
from . import views

urlpatterns = [
    path('candidates/', views.CandidatesList.as_view()),
    path('candidates/<str:candidate_id>/', views.CandidateDetail.as_view())
]
