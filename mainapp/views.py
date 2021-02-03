from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from . import models
from .forms import CandidateEvaluateForm, AddCandidateForm, ApprovementForm
from .decorators import auth_check,check_permissions

adm_dep = 0
committie = 1
chair = 2
secretary=3

@login_required(login_url = 'login')
def dashboardView(request):
    candidates = models.CandidateModel.objects.all()
    context={'candidates':candidates}
    return render(request, 'mainapp/dashboard.html', context)

@login_required(login_url = 'login')
@check_permissions(allowed_pos=[committie,chair])
def candidateView(request,uuid):

    evaluator = models.ProfileModel.objects.get(user = request.user)
    candidate = models.CandidateModel.objects.get(candidate_id = uuid)
    evaluation = models.EvaluationModel.objects.get(evaluator = evaluator, candidate=candidate)
    form = CandidateEvaluateForm(instance=evaluation)
    if request.method == "POST":
        form = CandidateEvaluateForm(request.POST,instance=evaluation)
        #, instance=evaluation
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form':form, 'candidate':candidate}

    return render(request, 'mainapp/profile-candidate.html', context)


@login_required(login_url = 'login')
@check_permissions(allowed_pos=[secretary])
def approveEvalView(request,uuid):

    evaluation = models.EvaluationModel.objects.get(evaluation_id = uuid)
    form = ApprovementForm(instance=evaluation)
    context = {'evaluation':evaluation}
    if request.method == "POST":
        form = ApprovementForm(request.POST, instance=evaluation)
        form.status = 'Approved'
        if request.POST['approved_by_secretary'] == 'on':
            evaluation.status = 'Approved'
            evaluation.save()
            return redirect('dashboard')
    context = {'form':form, 'evaluation':evaluation}
    return render(request, 'mainapp/approve_evaluation.html', context)



@login_required(login_url = 'login')
@check_permissions(allowed_pos=[adm_dep])
def createCandidateView(request):
    
    form = AddCandidateForm()
    if request.method == "POST":
        form = AddCandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save()
            #candidate = models.CandidateModel.objects.get(candidate_id = request.POST.uuid)
            evaluators_committie = models.ProfileModel.objects.filter(position = 1)
            
            evaluators_chair = models.ProfileModel.objects.filter(position = 2)
            for person in evaluators_committie:
                 models.EvaluationModel.objects.create(
                    evaluator = person,
                    candidate = candidate
                )
            for person in evaluators_chair:
                 models.EvaluationModel.objects.create(
                    evaluator = person,
                    candidate = candidate
                )

            return redirect('dashboard')
    context = {'form':form}

    return render(request, 'mainapp/admission-dept-page.html', context)

@login_required(login_url = 'login')
def infoView(request):
    publications = models.InformationModel.objects.all()
    context= {'publications':publications}
    return render(request, 'mainapp/info.html', context)

@login_required(login_url = 'login')
def contactsView(request):
    dept_members = models.ProfileModel.objects.filter(position = 0)
    committie = models.ProfileModel.objects.filter(position = 1)
    chairs = models.ProfileModel.objects.filter(position = 2)
    secretaries = models.ProfileModel.objects.filter(position = 3)
    context ={
        'dept_members':dept_members,
        'committie':committie,
        'chairs':chairs,
        'secretaries':secretaries,        
        }
    return render(request, 'mainapp/contacts.html', context)

@login_required(login_url = 'login')
def personalView(request):
    position = [
        'Admission department','Admission committie member',
        'Chair of the admission committie','School Secretary'
    ]
    context ={'position':position[request.user.profilemodel.position]}
    return render(request, 'mainapp/personal.html', context)

@auth_check
def loginView(request):
    context = {}

    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        else:
            messages.error(request, "Data is invalid")
            return render(request, 'mainapp/login.html', context)


    return render(request, 'mainapp/login.html', context)
    


def logoutView(request):
    logout(request)
    return redirect('login')
