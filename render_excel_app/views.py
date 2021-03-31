from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from auth_app.decorators import check_permissions
from auth_app.models import CustomUserModel
from render_excel_app.utils import (get_evaluation_data,
                                    generate_application_xlsx,
                                    save_application_zip,
                                    generate_interview_xlsx,
                                    save_interview_zip)


@login_required(login_url='login')
@check_permissions(allowed_pos=[CustomUserModel.SECRETARY])
def ApplicationEvalAsExcelView(request, evaluation_id):
    """
        Render application evaluation into excel and send back to client
    """
    evaluation = get_evaluation_data(evaluation_id,
                                     'application_evaluation')
    [wb, name] = generate_application_xlsx(evaluation)
    # set response type to excel file
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = \
        'attachment; filename=' \
        '{0}'.format(name)
    wb.save(response)
    return response
    # return HttpResponse("Here's the text of the Web page.")


@login_required(login_url='login')
@check_permissions(allowed_pos=[CustomUserModel.SECRETARY])
def InterviewEvalAsExcelView(request, evaluation_id):
    """
        Render interview evaluation into excel and send back to client
    """
    evaluation = get_evaluation_data(evaluation_id,
                                     'interview_evaluation')
    [wb, name] = generate_interview_xlsx(evaluation)
    # set response type to excel file
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = \
        'attachment; filename={0}' .format(name)
    wb.save(response)
    return response


@login_required(login_url='login')
@check_permissions(allowed_pos=[CustomUserModel.SECRETARY])
def zip_application_evaluations(request, candidate_id):
    """
        Render interview evaluation into excel and send back to client
    """

    [buffer, name] = save_application_zip(candidate_id)
    response = HttpResponse(buffer.getvalue())
    response['Content-Type'] = 'application/x-zip-compressed'
    response['Content-Disposition'] = 'attachment; filename={0}'.format(name)
    return response


@login_required(login_url='login')
@check_permissions(allowed_pos=[CustomUserModel.SECRETARY])
def zip_interview_evaluations(request, candidate_id):
    """
        Render interview evaluation into excel and send back to client
    """

    [buffer, name] = save_interview_zip(candidate_id)
    response = HttpResponse(buffer.getvalue())
    response['Content-Type'] = 'application/x-zip-compressed'
    response['Content-Disposition'] = 'attachment; filename={0}'.format(name)
    return response
