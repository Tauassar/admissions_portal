from django.shortcuts import get_object_or_404

import admission_periods_app.models


def get_current_admission_round():
    """
    returns active admission year
    """
    try:
        return admission_periods_app.models.AdmissionYearModel.objects \
            .filter(active=True).prefetch_related("rounds")[0].rounds.get(finished=False)
    except Exception:
        return


def get_current_admission_year():
    """
    returns active admission year
    """
    try:
        admission_year = admission_periods_app.models.\
            AdmissionYearModel.objects.get(active=True)
    except Exception:
        return
    return admission_year


def set_round_number():
    """
    Sets default value for admission round count
    (i.e. AdmissionRoundModel's round_number)
    """
    try:
        current_round_number = admission_periods_app.\
            AdmissionYearModel.objects.filter(active=True).\
            prefetch_related("rounds").round_number
        if current_round_number == admission_periods_app.\
                AdmissionRoundModel.MAX_ROUNDS:
            raise Exception(
                'Number of admissions rounds exceeded its max value')
        return current_round_number + 1
    except Exception as e:
        print(e)
        return None


def get_current_year_and_round():
    """
        get active admission year and round from database
    """
    admission_year = get_object_or_404(
        admission_periods_app.models.AdmissionYearModel, active=True)
    admission_round = admission_year.get_current_admission_round
    return [admission_year, admission_round]