from django.urls import path

from auth_app.views import ContactsView, PersonalView, ProfileView
from candidates_app.views import createCandidateView
from evaluations_app.views import approveEvalView, candidateEvaluateView
from mainapp.views import SecretaryView, ChairView, dashboardView
from help_information_app.views import InfoView


urlpatterns = [
    # mainapp
    path('', dashboardView, name='dashboard'),
    path('chair/', ChairView.as_view(), name='chair'),
    # path('chair/', ChairViewfunc, name='chair'),
    path('secretary/', SecretaryView.as_view(), name='secretary'),
    # info_app
    path('info/', InfoView.as_view(), name='info'),
    # auth_app
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('personal/', PersonalView.as_view(), name='personal'),
    path('profile/<str:uuid>/', ProfileView.as_view(), name='profile'),
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
]
