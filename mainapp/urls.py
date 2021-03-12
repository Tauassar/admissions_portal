from django.urls import path

from auth_app.views import profileView, personalView, contactsView
from candidates_app.views import createCandidateView
from evaluations_app.views import approveEvalView, candidateEvaluateView
from mainapp.views import SecretaryView, ChairView, dashboardView
from render_excel_app.views import (GetApplicationEvaluationAsExcelView,
                                    GetInterviewEvaluationAsExcelView)
from help_information_app.views import infoView


urlpatterns = [
    # mainapp
    path('', dashboardView, name='dashboard'),
    path('chair/', ChairView, name='chair'),
    path('secretary/', SecretaryView, name='secretary'),
    # info_app
    path('info/', infoView, name='info'),
    # auth_app
    path('contacts/', contactsView, name='contacts'),
    path('personal/', personalView, name='personal'),
    path('profile/<str:uuid>/', profileView, name='profile'),
    # evaluate_app
    path('candidate_evaluate/<str:uuid>/', candidateEvaluateView,
         name='candidate_evaluate'),
    path('approve_evaluation/<str:uuid>/', approveEvalView,
         name='approve_evaluation'),
    # candidate_app
    path('create_candidate/', createCandidateView,
         name='create_candidate'),
    path('observe_candidate/<str:candidate_id>/',
         createCandidateView, name='observe_candidate'),
    # excel_app
    path('excell_application/<str:evaluation_id>/',
         GetApplicationEvaluationAsExcelView,
         name='excel_application'),
    path('excell_interview/<str:evaluation_id>/',
         GetInterviewEvaluationAsExcelView, name='excel_interview')
]
