from django.urls import path

from render_excel_app.views import (ApplicationEvalAsExcelView,
                                    InterviewEvalAsExcelView,
                                    zip_application_evaluations,
                                    zip_interview_evaluations)

urlpatterns = [
    # excel_app
    path('application_eval/<str:evaluation_id>/',
         ApplicationEvalAsExcelView,
         name='excel_application'),
    path('interview_eval/<str:evaluation_id>/',
         InterviewEvalAsExcelView, name='excel_interview'),
    path('application_zip/<str:candidate_id>/',
         zip_application_evaluations, name='zip_applications'),
    path('interview_zip/<str:candidate_id>/',
         zip_interview_evaluations, name='zip_applications')
]