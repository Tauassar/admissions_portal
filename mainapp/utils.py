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
        if candidate.total_score >= threshold:
            candidate.student_list = admission_round.accepted_candidates_list
        else:
            continue
        candidate.save()
