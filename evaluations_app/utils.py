from django.core.exceptions import ObjectDoesNotExist


def actions_to_list(actions):
    converted_actions = []
    history_type = {
        '~': 'Updated ',
        '+': 'Added ',
        '-': 'Deleted ',
    }
    for action in actions:
        action_str = ''
        action_str += history_type[action.history_type]
        try:
            action_str += str(action.candidate)
        except AttributeError:
            action_str += '{0} {1}'.format(action.first_name, action.last_name)
        except (NameError, ObjectDoesNotExist):
            action_str += 'candidate'
            pass
        action_str += action.history_date.strftime(" %d.%m at %H:%M")
        converted_actions.append(action_str)
    return converted_actions


def get_total_interview_score(model):
    # calculate total score for given evaluation
    if not model.skip_evaluation:
        total = sum(
            [model.work_experience_goals * 2,
             model.research_interest_and_motivation * 2,
             model.understanding_of_major * 1.5,
             model.community_involvement * 1.5,
             model.interpersonal_skills * 1.5,
             model.english_level * 1.5]
        )
        return total
    else:
        return None


def get_total_application_score(model):
    candidate = model.evaluation.candidate
    gpa = getattr(candidate, 'gpa')
    school_rating = getattr(candidate, 'school_rating')
    research_experience = getattr(candidate, 'research_experience')
    total = sum(
        [model.relevancy,
         model.statement_of_purpose,
         model.recommendation_1,
         model.recommendation_2,
         model.relevant_degrees,
         school_rating,
         gpa * 7,
         research_experience * 5]
    )
    return total


def calculate_total_score(evaluations):
    application_total = 0
    interview_total = 0
    interview_count = 0
    try:
        for evaluation in evaluations:
            application_evaluation = evaluation.applicationevaluationmodel
            interview_evaluation = evaluation.interviewevaluationmodel
            application_total = \
                application_total + \
                get_total_application_score(application_evaluation)
            if not interview_evaluation.skip_evaluation:
                interview_total = \
                    interview_total + \
                    get_total_interview_score(interview_evaluation)
                interview_count = interview_count + 1
        return (application_total / len(evaluations)) * 0.4 + \
               (interview_total / interview_count) * 0.6
    except Exception:
        pass


def queryset_to_dict(queryset, exclude=None):
    fields = queryset._meta.get_fields(include_hidden=False)
    print(fields)
    instance_dict = {}
    for field in fields:
        try:
            if field.name in exclude:
                continue
            key = field.verbose_name
            instance_dict[key] = getattr(queryset, field.name)
        except Exception:
            continue
    return instance_dict
