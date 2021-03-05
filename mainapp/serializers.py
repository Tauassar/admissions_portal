from rest_framework import serializers
from .models import CandidateModel

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateModel
        exclude = ['total_score', 'candidate_status', 'evaluation_finished', 'student_list', 'admission_round']
