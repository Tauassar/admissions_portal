from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.ProfileModel)
admin.site.register(models.CandidateModel)
admin.site.register(models.CandidateEvaluationModel)
admin.site.register(models.InformationModel)
admin.site.register(models.CandidateTestingInformationModel)
admin.site.register(models.CandidateEducationModel)
admin.site.register(models.StaffListModel)
admin.site.register(models.AdmissionRoundModel)
admin.site.register(models.AdmissionYearModel)