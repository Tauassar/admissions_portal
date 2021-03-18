from rest_framework import serializers

from auth_app.models import CustomUserModel
from candidates_app.models import (CandidateModel,
                                   CandidateEducationModel,
                                   CandidateTestsModel)
from evaluations_app.models import (ApplicationEvaluationModel,
                                    InterviewEvaluationModel,
                                    CandidateEvaluationModel)


# access candidate model
class CandidateEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateEducationModel
        exclude = ['candidate']


class CandidateTestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateTestsModel
        exclude = ['candidate']


class CandidateSerializer(serializers.ModelSerializer):
    testing_info = CandidateTestsSerializer(source="testing",
                                            read_only=True)
    education_info = CandidateEducationSerializer(many=True,
                                                  source="education",
                                                  read_only=True)

    class Meta:
        model = CandidateModel
        exclude = ['total_score',
                   'candidate_status',
                   'evaluation_finished',
                   'student_list',
                   'admission_round',
                   'gpa',
                   'school_rating',
                   'research_experience']

    # Custom create()
    def create(self, validated_data):
        # retrieve dependant models data from validated data
        testing_info = validated_data.pop('testing')
        education_info = validated_data.pop('education')
        # create candidate
        candidate = CandidateModel.objects.create(**validated_data)
        # create dependant models
        CandidateTestsModel.objects.create(candidate=candidate,
                                           **testing_info)
        CandidateEducationModel.objects.create(candidate=candidate,
                                               **education_info)
        # Return a candidate instance
        return candidate


# access candidate model
class CandidateDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateModel
        fields = ['first_name',
                  'last_name',
                  'candidate_id',
                  'applying_degree',
                  'admission_round']


# dashboard serializers
class ApplicationEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationEvaluationModel
        exclude = ['evaluation']


class InterviewEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewEvaluationModel
        exclude = ['evaluation']


class EvaluatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ['first_name',
                  'last_name',
                  'staff_id'
                  ]
        read_only_fields = (
            'first_name',
            'last_name',
            'staff_id')


class CandidateDashboard(serializers.ModelSerializer):
    class Meta:
        model = CandidateModel
        fields = [
            'first_name',
            'last_name',
            'candidate_id'
        ]
        read_only_fields = (
            'first_name',
            'last_name',
            'candidate_id')


class EvaluationSerializer(serializers.ModelSerializer):
    candidate = CandidateDashboard()
    evaluator = EvaluatorSerializer()

    class Meta:
        model = CandidateEvaluationModel
        fields = ['evaluation_id',
                  'evaluation_status',
                  'candidate',
                  'evaluator', ]
        read_only_fields = ('evaluation_id',
                            'evaluation_status',
                            'candidate',
                            'evaluator',)
