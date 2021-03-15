from django.urls import path

from render_excel_app.views import (ApplicationEvalAsExcelView,
                                    InterviewEvalAsExcelView)

urlpatterns = [
    # excel_app
    path('application_eval/<str:evaluation_id>/',
         ApplicationEvalAsExcelView,
         name='excel_application'),
    path('interview_eval/<str:evaluation_id>/',
         InterviewEvalAsExcelView, name='excel_interview')
]