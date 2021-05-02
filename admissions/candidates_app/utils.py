from admission_periods_app.utils import get_current_year_and_round


def file_directory_path(instance, filename):
    """
    sets path of the uploaded files of CandidateModel
    to a folder named using candidate data
    """
    return '{0}_{1}_{2}/{3}'.format(instance.first_name, instance.last_name,
                                    instance.date_created.strftime('%d_%m_%Y'),
                                    filename)


def get_current_candidates(*args, **kwargs):
    """
    sets path of the uploaded files of CandidateModel
    to a folder named using candidate data
    """
    year, c_round = get_current_year_and_round()
    return year.current_candidates


def candidate_unfinish(candidate):
    if candidate.evaluation_finished:
        candidate.evaluation_finished = False
        candidate.save()
