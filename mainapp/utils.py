import logging

from django.db.models import Q

from candidates_app.models import DEGREE


# Get an instance of a logger
logger = logging.getLogger(__name__)


def clear_list(candidates, admission_year):
    for candidate in candidates:
        candidate.student_list = admission_year.current_candidates
        candidate.save()


def compose_lists(threshold, admission_year, admission_round):
    accepted_list = admission_round. \
        accepted_candidates_list.candidates.all()
    rejected_list = admission_round. \
        rejected_candidates_list.candidates.all()
    candidates = admission_year. \
        current_candidates.candidates.all()
    if accepted_list or rejected_list:
        clear_list(accepted_list, admission_year)
        clear_list(rejected_list, admission_year)
    for candidate in candidates:
        try:
            if candidate.total_score >= threshold:
                candidate.student_list = \
                    admission_round.accepted_candidates_list
            else:
                continue
        except TypeError:
            logger.warning("Candidates evaluation is not finished")
            logger.warning("Candidate: {0}".format(candidate.first_name))
        candidate.save()


def check_valid_queryparameter(param):
    return param != '' \
           and param is not None \
           and param != 'Choose...'


def parse_degree(degree):
    for tup in DEGREE:
        if tup[1] == degree:
            return tup[0]


def dashboard_filters(request, qs, is_eval):
    firstname = request.GET.get('firstname')
    surname = request.GET.get('surname')
    degree = request.GET.get('degree')
    status = request.GET.get('status')
    sorting = request.GET.get('sorting')

    # filter name
    if not is_eval:
        if check_valid_queryparameter(firstname):
            qs = qs.filter(Q(first_name__icontains=firstname)).distinct()
    else:
        if check_valid_queryparameter(firstname):
            qs = qs.filter(
                Q(candidate__first_name__icontains=firstname)).distinct()
    # second name
    if not is_eval:
        if check_valid_queryparameter(surname):
            qs = qs.filter(Q(last_name__icontains=surname)).distinct()
    else:
        if check_valid_queryparameter(surname):
            qs = qs.filter(
                Q(candidate__last_name__icontains=surname)).distinct()

    # filter degree
    if not is_eval:
        if check_valid_queryparameter(degree):
            qs = qs.filter(applying_degree=parse_degree(degree)).distinct()
    else:
        if check_valid_queryparameter(degree):
            qs = qs.filter(
                candidate__applying_degree=parse_degree(degree)).distinct()
    # check status
    if is_eval:
        if check_valid_queryparameter(status):
            logger.debug(qs[0].evaluation_status)
            qs = qs.filter(evaluation_status=status)
    # sort
    if not is_eval:
        if check_valid_queryparameter(sorting):
            if sorting == "-major":
                qs = qs.order_by('-applying_degree')
            elif sorting == "major":
                qs = qs.order_by('applying_degree')
            elif sorting == "-name":
                qs = qs.order_by('-first_name')
            elif sorting == "name":
                qs = qs.order_by('first_name')
    else:
        if check_valid_queryparameter(sorting):
            if sorting == "-major":
                qs = qs.order_by('-candidate__applying_degree')
            elif sorting == "major":
                qs = qs.order_by('candidate__applying_degree')
            elif sorting == "-name":
                qs = qs.order_by('-candidate__first_name')
            elif sorting == "name":
                qs = qs.order_by('candidate__first_name')
    return qs
