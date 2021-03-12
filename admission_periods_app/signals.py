from django.db.models.signals import post_save

from admission_periods_app.models import (AdmissionYearModel,
                                          AdmissionRoundModel,
                                          StaffListModel,
                                          StudentList)


def admission_year_created(sender, instance, created, **kwargs):
    if created:
        AdmissionRoundModel.objects.create(admission_year=instance,
                                           round_number=1)
        StaffListModel.objects.create(admission_year=instance)
        active_years = AdmissionYearModel.objects.filter(active=True).exclude(
            id=instance.id)
        for year in active_years:
            year.active = False
            year.save()




def create_waiting_list(sender, created, instance, **kwargs):
    if created:
        instance.current_candidates = StudentList.objects.create(
            list_type=StudentList.WAITING_LIST)
        instance.save()


def create_candidate_lists(sender, created, instance, **kwargs):
    if created:
        print("signal create_candidate_lists initiated")
        instance.accepted_candidates_list = StudentList.objects.create(
            list_type=StudentList.ACCEPTED)
        instance.rejected_candidates_list = StudentList.objects.create(
            list_type=StudentList.REJECTED)
        instance.save()


def admission_round_created(sender, instance, created, **kwargs):
    """
        set old admission periods to false when new period is created
    """
    if created:
        active_rounds = AdmissionRoundModel.objects.filter(
            finished=False).exclude(id=instance.id)
        for subject in active_rounds:
            subject.finished = True
            subject.save()


post_save.connect(admission_year_created, sender=AdmissionYearModel)
post_save.connect(create_waiting_list, sender=AdmissionYearModel)
post_save.connect(create_candidate_lists, sender=AdmissionRoundModel)
post_save.connect(admission_round_created, sender=AdmissionRoundModel)
