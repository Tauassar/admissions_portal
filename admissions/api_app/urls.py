from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(
    'evaluations', views.RoundEvaluationsViewSet, "evaluations_api")
router.register('candidate', views.CandidateDetail, "candidate_api")


urlpatterns = [
    path('', include(router.urls)),
    path('candidates/',
         views.RoundCandidates.as_view(),
         name='candidates_api')
    # path('candidate/<str:candidate_id>/',
    #      views.CandidateDetail.as_view(),
    #      name='candidate_detail_api')
]
