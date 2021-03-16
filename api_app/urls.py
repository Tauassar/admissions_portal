from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('evaluations', views.RoundEvaluationsViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('candidates/', views.RoundCandidates.as_view()),
    path('candidates/<str:candidate_id>/',
         views.CandidateDetail.as_view())
]
