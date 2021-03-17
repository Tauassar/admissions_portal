from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from admission_periods_app.models import AdmissionYearModel
from auth_app.models import CustomUserModel
from candidates_app.models import CandidateModel
from mainapp.mixins import PositionMixin
from .serializers import (CandidateSerializer,
                          EvaluationSerializer,
                          CandidateDashboardSerializer)


class CandidateDetail(PositionMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a Candidate instance.
    """
    permission_groups = [CustomUserModel.ADMISSION_DEPARTMENT]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_url_kwarg = 'candidate_id'
    lookup_field = 'candidate_id'
    serializer_class = CandidateSerializer

    def get_queryset(self):
        return CandidateModel.objects.all()


# DASHBOARD VIEWS
class RoundCandidates(PositionMixin, ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_groups = [CustomUserModel.ADMISSION_DEPARTMENT]
    queryset = AdmissionYearModel.objects.get(active=True).rounds.get(finished=False).candidates.all()
    serializer_class = CandidateDashboardSerializer


class RoundEvaluationsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_groups = [CustomUserModel.COMMITTEE_MEMBER,
                         CustomUserModel.COMMITTEE_CHAIR,
                         CustomUserModel.SECRETARY]
    queryset = AdmissionYearModel.objects.get(active=True) \
        .rounds.get(finished=False).evaluations.all()
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
