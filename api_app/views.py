from rest_framework import permissions, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.mixins import (CreateModelMixin,
                                   RetrieveModelMixin,
                                   DestroyModelMixin,
                                   UpdateModelMixin)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import GenericViewSet

from admission_periods_app.models import AdmissionYearModel
from auth_app.models import CustomUserModel
from candidates_app.models import CandidateModel
from mainapp.mixins import PositionMixin
from .serializers import (CandidateSerializer,
                          EvaluationSerializer,
                          CandidateDashboardSerializer)


class CandidateDetail(PositionMixin,
                      CreateModelMixin,
                      RetrieveModelMixin,
                      DestroyModelMixin,
                      UpdateModelMixin,
                      GenericViewSet):
    """
    Retrieve, create, update or delete a Candidate instance.
    """
    permission_groups = [CustomUserModel.ADMISSION_DEPARTMENT]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_url_kwarg = 'candidate_id'
    lookup_field = 'candidate_id'
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = CandidateSerializer
    queryset = CandidateModel.objects.all()


# DASHBOARD VIEWS
class RoundCandidates(PositionMixin, ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_groups = [CustomUserModel.ADMISSION_DEPARTMENT]
    serializer_class = CandidateDashboardSerializer

    def get_queryset(self):
        return AdmissionYearModel.objects.get(active=True)\
            .rounds.get(finished=False).candidates.all()


class RoundEvaluationsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_groups = [CustomUserModel.COMMITTEE_MEMBER,
                         CustomUserModel.COMMITTEE_CHAIR,
                         CustomUserModel.SECRETARY]
    queryset = AdmissionYearModel.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return AdmissionYearModel.objects.get(active=True)\
            .rounds.get(finished=False).evaluations.all()
