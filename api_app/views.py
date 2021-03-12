from rest_framework import generics, permissions

from candidates_app.models import CandidateModel
from .serializers import CandidateSerializer


class CandidateDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a Candidate instance.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_url_kwarg = 'candidate_id'
    lookup_field = 'candidate_id'
    serializer_class = CandidateSerializer

    def get_queryset(self):
        return CandidateModel.objects.all()


class CandidatesList(generics.ListCreateAPIView):
    """
        Returns all candidate objects that are stored in the database
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = CandidateModel.objects.all()
    serializer_class = CandidateSerializer
