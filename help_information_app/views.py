from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from help_information_app.models import InformationModel


@login_required(login_url='login')
def infoView(request):
    publications = InformationModel.objects.all()
    context = {'publications': publications}
    return render(request, 'help_information_app/info.html', context)
