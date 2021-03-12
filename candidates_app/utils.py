def file_directory_path(instance, filename):
    """
    sets path of the uploaded files of CandidateModel
    to a folder named using candidate data
    """
    return '{0}_{1}_{2}/{3}'.format(instance.first_name, instance.last_name,
                                    instance.date_created.strftime('%d_%m_%Y'),
                                    filename)
