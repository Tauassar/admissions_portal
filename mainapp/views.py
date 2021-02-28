import time

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import inlineformset_factory

from .models import CustomUserModel,CandidateModel,CandidateEvaluationModel,InformationModel,AdmissionYearModel,ApplicationEvaluationModel, InterviewEvaluationModel
from .forms import CandidateEvaluateForm, AddCandidateForm, ApprovementForm, AdmissionRoundForm
from .decorators import auth_check,check_permissions

adm_dep = 0
committie = 1
chair = 2
secretary=3

def getCurrentAdmissionsYearAndRound():
    admission_year = get_object_or_404(AdmissionYearModel, active=True)
    admission_round = admission_year.getCurrentAdmissionRound()
    return [admission_year, admission_round]
    

@login_required(login_url = 'login')
def dashboardView(request):
    admission_year, admission_round = getCurrentAdmissionsYearAndRound()    
    try:
        candidates = admission_round.candidatemodel_set.all()
        evaluations = CandidateEvaluationModel.objects.all()
    except (ObjectDoesNotExist, AttributeError):
        return render(request, 'mainapp/main_dashboard.html')
    context={
        'candidates':candidates,
        'evaluations':evaluations,
    }
    return render(request, 'mainapp/main_dashboard.html', context)

@login_required(login_url = 'login')
@check_permissions(allowed_pos=[committie,chair])
def candidateEvaluateView(request,uuid):
    evaluator = request.user
    candidate = get_object_or_404(CandidateModel, candidate_id = uuid)
    evaluation = get_object_or_404(CandidateEvaluationModel, evaluator = evaluator, candidate=candidate)
    form = CandidateEvaluateForm(instance=evaluation)
    application_formset = inlineformset_factory(CandidateEvaluationModel, ApplicationEvaluationModel,fields = '__all__', can_delete = False)
    interview_formset = inlineformset_factory(CandidateEvaluationModel, InterviewEvaluationModel,fields = '__all__', can_delete = False)
    if request.method == "POST":
        form = CandidateEvaluateForm(request.POST,instance=evaluation)
        #, instance=evaluation
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {
        'application_formset':application_formset,
        'interview_formset':interview_formset,
        'candidate':candidate}

    return render(request, 'mainapp/evaluate_candidate.html', context)

@login_required(login_url = 'login')
@check_permissions(allowed_pos=[secretary])
def approveEvalView(request,uuid):
    evaluation = get_object_or_404(CandidateEvaluationModel, evaluation_id = uuid)
    form = ApprovementForm(instance=evaluation)

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
def createCandidateView(request, id=None):
    admission_year, admission_round = getCurrentAdmissionsYearAndRound()
    if id is not None:
        candidate = get_object_or_404(CandidateModel, candidate_id = id)
        form = AddCandidateForm(instance=candidate)
    else:
        form = AddCandidateForm()
        
    if request.method == "POST":
        form = AddCandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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
    admission_year = get_object_or_404(AdmissionYearModel, active=True)
    staff_list = admission_year.getStaffList()
    dept_members = staff_list.filter(position = 0)
    committie = staff_list.filter(position = 1)
    chairs = staff_list.filter(position = 2)
    secretaries = staff_list.filter(position = 3)
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
        print("\n\n\nPOST INIT")
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            print("\n\n\nPass changed")
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('personal')
        else:
            print("\n\n\nError")
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    context ={
        'position':position[request.user.position],
        'form': form,
        'user':request.user
        }
    return render(request, 'mainapp/personal.html', context)


@login_required(login_url = 'login')
def profileView(request, uiid):
    position = [
        'Admission department','Admission committie member',
        'Chair of the admission committie','School Secretary'
    ]
    
    if uiid.replace(" ", "")==str(request.user.staff_id):
        return redirect('personal')
    user = get_object_or_404(CustomUserModel, staff_id = uiid)

    context ={
        'position':position[request.user.position],
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
            messages.error(request, "Please check username and password")
            return render(request, 'mainapp/login.html', context)


    return render(request, 'mainapp/login.html', context)
    


def logoutView(request):
    logout(request)
    return redirect('login')

@login_required(login_url = 'login')
@check_permissions(allowed_pos=[chair])
def ChairView(request):
    admission_year, admission_round = getCurrentAdmissionsYearAndRound()
    
    try:
        candidates = admission_round.candidatemodel_set.all()
        profile = request.user
    except (ObjectDoesNotExist, AttributeError):
        return render(request, 'mainapp/dashboard.html')

    form = AdmissionRoundForm()
    if request.method == "POST":
        form = AdmissionRoundForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {
        'admissiou_round':admission_round, 
        'form':form,
        'candidates':candidates,
        'total_candidates':len(candidates)
      }
    return render(request, 'mainapp/chair_template.html', context)

