from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from help_information_app.models import InformationModel


class InfoView(LoginRequiredMixin, ListView):
    model = InformationModel
    context_object_name = 'publications'
    template_name = 'help_information_app/info.html'
