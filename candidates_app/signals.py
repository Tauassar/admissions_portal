from django.db.models.signals import post_save

from admission_periods_app.models import AdmissionYearModel
from candidates_app.models import CandidateModel


def set_candidate_list(sender, instance, created, **kwargs):
    if created:
        try:
            current_admission_year = AdmissionYearModel.objects.get(
                active=True)
        except Exception:
            raise Exception("No active admission year found")
        instance.student_list = current_admission_year.current_candidates
        instance.save()


post_save.connect(set_candidate_list, sender=CandidateModel)
