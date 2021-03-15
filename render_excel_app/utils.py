from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from candidates_app.models import DEGREE
from evaluations_app.models import CandidateEvaluationModel


def write_candidate_evaluator_data(work_sheet, candidate, evaluator):
    # candidate general info
    work_sheet['B4'] = candidate.first_name
    work_sheet['C4'] = candidate.last_name
    work_sheet['D4'] = candidate.candidate_id
    work_sheet['F4'] = DEGREE[candidate.applying_degree][1]
    # evaluator general info
    work_sheet['B5'] = evaluator.first_name
    work_sheet['C5'] = evaluator.last_name
    work_sheet['D5'] = str(evaluator.staff_id)


def get_evaluation_data(evaluation_id=None,
                        evaluation_type='application_evaluation'):
    try:
        return CandidateEvaluationModel.objects.\
            select_related('candidate',
                           'evaluator',
                           evaluation_type
                           ).get(evaluation_id=evaluation_id)
    except ObjectDoesNotExist:
        raise Http404("No {0} found matching the query".format(
            CandidateEvaluationModel._meta.verbose_name
        ))
