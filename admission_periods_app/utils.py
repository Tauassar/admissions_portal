from django.http import Http404
from django.shortcuts import get_object_or_404

import admission_periods_app.models as models


def get_current_admission_round():
    """
    returns active admission year
    """
    try:
        return models.AdmissionYearModel.objects \
            .filter(active=True).prefetch_related("rounds")[0] \
            .rounds.get(finished=False)
    except models.AdmissionYearModel.DoesNotExist:
        raise Http404("No {0} found matching the query".format(
            models.AdmissionYearModel._meta.verbose_name
        ))


def get_current_admission_year():
    """
    returns active admission year
    """
    pass
    try:
        return models.AdmissionYearModel.objects.get(active=True).id
    except models.AdmissionYearModel.DoesNotExist:
        return None
        raise Http404("No {0} found matching the query".format(
            models.AdmissionYearModel._meta.verbose_name
        ))


def set_round_number():
    """
    Sets default value for admission round count
    (i.e. AdmissionRoundModel's round_number)
    """
    try:
        current_round_number = models.AdmissionYearModel.objects\
            .filter(active=True).prefetch_related("rounds")[0]\
            .rounds.get(finished=False).round_number
        if current_round_number == models.AdmissionRoundModel.MAX_ROUNDS:
            # raise Exception(
            #     'Number of admissions rounds exceeded its max value')
            pass
        return current_round_number + 1
    except IndexError:
        return 1
    except models.AdmissionYearModel.DoesNotExist:
        raise Http404("No {0} found matching the query".format(
            models.AdmissionYearModel._meta.verbose_name
        ))


def get_current_year_and_round():
    """
        get active admission year and round from database
    # """
    admission_year = get_object_or_404(
        models.AdmissionYearModel, active=True)
    admission_round = admission_year.get_current_admission_round
    return [admission_year, admission_round]


def access_candidates_db(queryset):
    try:
        return queryset.candidates.all()
    except queryset.DoesNotExist:
        raise Http404("No {0} found matching the query".format(
            queryset._meta.verbose_name
        ))


def get_candidates(admission_year, admission_round):
    waiting_list = access_candidates_db(admission_year.current_candidates)
    accepted = access_candidates_db(admission_round.accepted_candidates_list)
    candidates = waiting_list | accepted
    evaluated_count = candidates.filter(evaluation_finished=True).count()
    non_evaluated_count = candidates.exclude(evaluation_finished=True).count()
    return candidates, evaluated_count, non_evaluated_count
