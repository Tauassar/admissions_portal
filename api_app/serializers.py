import json
import logging

from rest_framework import serializers

from auth_app.models import CustomUserModel
from candidates_app.models import (CandidateModel,
                                   CandidateEducationModel,
                                   CandidateTestsModel)
from evaluations_app.models import (ApplicationEvaluationModel,
                                    InterviewEvaluationModel,
                                    CandidateEvaluationModel)

# Get an instance of a logger
logger = logging.getLogger(__name__)


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
                                            allow_null=True,
                                            required=False)
    education_info = CandidateEducationSerializer(many=True,
                                                  source="education",
                                                  allow_null=True,
                                                  required=False)

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

    def to_internal_value(self, data):
        validated_data = super(CandidateSerializer, self)\
            .to_internal_value(data)
        testing = CandidateTestsSerializer(
            json.loads((data.pop("testing")[0])))
        education = CandidateEducationSerializer(
            json.loads((data.pop("education")[0])), many=True)
        logger.debug("testing info: {0}".format(str(testing.data)))
        logger.debug("education info: {0}".format(str(education.data)))
        validated_data['testing'] = testing.data
        validated_data['education'] = education.data
        return validated_data

    # Custom create()
    def create(self, validated_data):
        # retrieve dependant models data from validated data
        logger.debug("validated data:"+str(validated_data))

        testing_info = validated_data.pop('testing')
        education_info = validated_data.pop('education')
        # create candidate
        candidate = CandidateModel.objects.create(**validated_data)
        # create dependant models
        CandidateTestsModel.objects.create(candidate=candidate,
                                           **testing_info)
        objs = [
            CandidateEducationModel(
                candidate=candidate,
                **education_instance
            )
            for education_instance in education_info
        ]
        CandidateEducationModel.objects.bulk_create(objs)
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
