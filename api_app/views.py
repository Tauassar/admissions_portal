import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.mixins import (CreateModelMixin,
                                   RetrieveModelMixin,
                                   DestroyModelMixin,
                                   UpdateModelMixin)
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from admission_periods_app.models import AdmissionYearModel, StudentList
from admission_periods_app.utils import get_current_year_and_round
from auth_app.models import CustomUserModel
from candidates_app.models import CandidateModel
from mainapp.mixins import PositionMixin
from .serializers import (CandidateSerializer,
                          EvaluationSerializer,
                          CandidateDashboardSerializer)

logger = logging.getLogger(__name__)


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
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    serializer_class = CandidateSerializer
    queryset = CandidateModel.objects.all()

    def create(self, request, *args, **kwargs):
        logger.info(request)
        return super(CandidateDetail, self).create(request, *args, **kwargs)

    @action(methods=['GET'], detail=True)
    def raise_up(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            admission_year, admission_round = get_current_year_and_round()
            curr_list = instance.student_list
            if curr_list.list_type == StudentList.ACCEPTED:
                logger.info("candidate {0} raised to {1}".format(
                    instance.candidate_id, instance.student_list))
            #     TODO enroll to the program
            elif curr_list.list_type == StudentList.WAITING_LIST:
                instance.student_list = \
                    admission_round.accepted_candidates_list
                logger.info("candidate {0} raised to {1}".format(
                    instance.candidate_id, instance.student_list))
            else:
                if instance.get_score() > instance.admission_round.threshold:
                    instance.student_list = \
                        admission_round.accepted_candidates_list
                    logger.info("candidate {0} raised to {1}".format(
                        instance.candidate_id, instance.student_list))
                else:
                    instance.student_list = admission_year.current_candidates
                    logger.info("candidate {0} raised to {1}".format(
                        instance.candidate_id, instance.student_list))
            instance.save()
            logger.debug("instance saved")
        except ObjectDoesNotExist as e:
            logger.warning(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            logger.warning(e)
            return Response(
                "Either threshold or candidate evaluation is not finished",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def move_down(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            admission_year, admission_round = get_current_year_and_round()
            curr_list = instance.student_list
            if curr_list.list_type == StudentList.ACCEPTED:
                instance.student_list = \
                    admission_round.rejected_candidates_list
                logger.info("candidate {0} set down to {1}".format(
                    instance.candidate_id, instance.student_list))
                instance.save()
                logger.debug("instance saved")
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(
                    "Candidate not in accepted list",
                    status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            logger.warning(e)
            return Response(status=status.HTTP_404_NOT_FOUND)


# DASHBOARD VIEWS
class RoundCandidates(PositionMixin, ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_groups = [CustomUserModel.ADMISSION_DEPARTMENT]
    serializer_class = CandidateDashboardSerializer

    def get_queryset(self):
        return AdmissionYearModel.objects.get(active=True) \
            .rounds.get(finished=False).candidates.all()


class RoundEvaluationsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_groups = [CustomUserModel.COMMITTEE_MEMBER,
                         CustomUserModel.COMMITTEE_CHAIR,
                         CustomUserModel.SECRETARY]
    queryset = AdmissionYearModel.objects.all()
    serializer_class = EvaluationSerializer

    def get_queryset(self):
        return AdmissionYearModel.objects.get(active=True) \
            .rounds.get(finished=False).evaluations.all()
