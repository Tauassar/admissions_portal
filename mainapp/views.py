from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .models import ProfileModel, CandidateModel,EvaluationModel,InformationModel
from .forms import CandidateEvaluateForm, AddCandidateForm, ApprovementForm
from .decorators import auth_check,check_permissions

adm_dep = 0
committie = 1
chair = 2
secretary=3

@login_required(login_url = 'login')
def dashboardView(request):
    candidates = CandidateModel.objects.all()
    profile = ProfileModel.objects.get(user = request.user)
    evaluations = EvaluationModel.objects.all()
    context={
        'candidates':candidates,
        'position':profile.position,
        'evaluations':evaluations
    }
    return render(request, 'mainapp/dashboard.html', context)

@login_required(login_url = 'login')
@check_permissions(allowed_pos=[committie,chair])
def candidateEvaluateView(request,uuid):

    evaluator = ProfileModel.objects.get(user = request.user)
    candidate = CandidateModel.objects.get(candidate_id = uuid)
    evaluation = EvaluationModel.objects.get(evaluator = evaluator, candidate=candidate)
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
@check_permissions(allowed_pos=[adm_dep])
def observeCandidateView(request,uuid):

    candidate = CandidateModel.objects.get(candidate_id = uuid)
    context = {'candidate':candidate}
    return render(request, 'mainapp/view_candidate.html', context)


@login_required(login_url = 'login')
@check_permissions(allowed_pos=[secretary])
def approveEvalView(request,uuid):

    evaluation = EvaluationModel.objects.get(evaluation_id = uuid)
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
            #candidate = CandidateModel.objects.get(candidate_id = request.POST.uuid)
            evaluators_committie = ProfileModel.objects.filter(position = 1)
            
            evaluators_chair = ProfileModel.objects.filter(position = 2)
            for person in evaluators_committie:
                 EvaluationModel.objects.create(
                    evaluator = person,
                    candidate = candidate
                )
            for person in evaluators_chair:
                 EvaluationModel.objects.create(
                    evaluator = person,
                    candidate = candidate
                )

            return redirect('dashboard')
    context = {'form':form}

    return render(request, 'mainapp/create_candidate.html', context)

@login_required(login_url = 'login')
def infoView(request):
    publications = InformationModel.objects.all()
    context= {'publications':publications}
    return render(request, 'mainapp/info.html', context)

@login_required(login_url = 'login')
def contactsView(request):
    dept_members = ProfileModel.objects.filter(position = 0)
    committie = ProfileModel.objects.filter(position = 1)
    chairs = ProfileModel.objects.filter(position = 2)
    secretaries = ProfileModel.objects.filter(position = 3)
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


    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('personal')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    context ={
        'position':position[request.user.profilemodel.position],
        'form': form
        }
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
