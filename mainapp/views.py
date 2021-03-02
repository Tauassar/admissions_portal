from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import auth_check,check_permissions
from .models import (
    CustomUserModel,
    CandidateModel,
    CandidateEvaluationModel,
    InformationModel,
    AdmissionYearModel,
    ApplicationEvaluationModel,
    InterviewEvaluationModel)
from .forms import (
    SecretaryEvaluationForm,
    AddCandidateForm,
    ApprovementForm,
    AdmissionRoundForm,
    ApplicationFormset,
    InterviewFormset,
    TestingFormset,
    EducationFormset)

'''
    TODO: add committie report error button
        secretary comments
        forgot pass
        mail send
        different dashboards for different users
        recent actions
'''

ADMISSION_DEPARTMENT = 0
COMMITTIE_MEMBER = 1
COMMITIE_CHAIR = 2
SECRETARY=3
POSITIONS = [
    'Admission department',
    'Admission committie member',
    'Chair of the admission committie',
    'School Secretary'
]
def getCurrentAdmissionsYearAndRound():
    admission_year = get_object_or_404(AdmissionYearModel, active=True)
    admission_round = admission_year.getCurrentAdmissionRound()
    return [admission_year, admission_round]


@login_required(login_url = 'login')
def dashboardView(request):
    admission_year, admission_round = getCurrentAdmissionsYearAndRound()    
    try:
        candidates = admission_round.candidatemodel_set.all()
        evaluations = admission_round.candidateevaluationmodel_set.all()
        committie_evaluations = evaluations.exclude(evaluation_status=CandidateEvaluationModel.approved)
    except (ObjectDoesNotExist, AttributeError):
        return render(request, 'mainapp/main_dashboard.html')
    context={
        'candidates':candidates,
        'evaluations':committie_evaluations,
        'admission_round': admission_round.round_number
    }
    return render(request, 'mainapp/main_dashboard.html', context)


@login_required(login_url = 'login')
@check_permissions(allowed_pos=[COMMITTIE_MEMBER,COMMITIE_CHAIR])
def candidateEvaluateView(request,uuid):
    evaluator = request.user
    candidate = get_object_or_404(CandidateModel, candidate_id = uuid)
    evaluation = get_object_or_404(
        CandidateEvaluationModel,
        evaluator = evaluator,
        candidate=candidate)
    application_formset = ApplicationFormset(instance=evaluation)
    interview_formset = InterviewFormset(instance=evaluation)
    if request.method == "POST":
        application_formset = ApplicationFormset(request.POST, instance=evaluation)
        interview_formset = InterviewFormset(request.POST, instance=evaluation)
        if application_formset.is_valid() and interview_formset.is_valid():
            evaluation.status = CandidateEvaluationModel.in_progress
            evaluation.save()
            application_formset.save()
            interview_formset.save()
            return redirect('dashboard')
    context = {
        'application_formset':application_formset,
        'interview_formset':interview_formset,
        'candidate':candidate}

    return render(request, 'mainapp/evaluate_candidate.html', context)

def queryset_to_dict(queryset, exclude=None):
    fields = queryset._meta.get_fields(include_hidden=False)
    print(fields)
    instance_dict = {}
    for field in fields:
        try:
            if field.name in exclude:
                continue
            key = field.verbose_name
            instance_dict[key] = getattr(queryset, field.name)
        except Exception as e:
            continue
    return instance_dict

@login_required(login_url = 'login')
@check_permissions(allowed_pos=[SECRETARY])
def approveEvalView(request,uuid):
    evaluation = get_object_or_404(CandidateEvaluationModel, evaluation_id = uuid)
    application_evaluation = get_object_or_404(ApplicationEvaluationModel, evaluation=evaluation)
    interview_evaluation = get_object_or_404(InterviewEvaluationModel, evaluation=evaluation)
    application_evaluation_dict = queryset_to_dict(
        application_evaluation,
        exclude=['evaluation', 'id'])
    if not interview_evaluation.skip_evaluation:
        interview_evaluation_dict =  queryset_to_dict(
            interview_evaluation,
            exclude=['evaluation', 'id'])
    else:
        interview_evaluation_dict =  None
    approve_form = ApprovementForm()
    evaluate_form = SecretaryEvaluationForm(instance=evaluation.candidate)
    if request.method == "POST":
        approve_form = ApprovementForm(request.POST)
        evaluate_form = SecretaryEvaluationForm(request.POST, instance=evaluation.candidate)
        if approve_form.is_valid() and evaluate_form.is_valid():
            evaluation.evaluation_status = approve_form.cleaned_data['status']
            evaluate_form.save()
            evaluation.save()
            return redirect('dashboard')

    context = {
        'evaluate_form':evaluate_form, 
        'approve_form':approve_form,
        'application_evaluation_dict':application_evaluation_dict,
        'interview_evaluation_dict':interview_evaluation_dict,
        'evaluation':evaluation}

    return render(request, 'mainapp/approve_evaluation.html', context)


@login_required(login_url = 'login')
@check_permissions(allowed_pos=[ADMISSION_DEPARTMENT])
def createCandidateView(request, candidate_id=None):
    if id is not None:
        candidate = get_object_or_404(CandidateModel, candidate_id=candidate_id)
        form = AddCandidateForm(instance=candidate)
        testing_formset = TestingFormset(instance=candidate)
        education_formset = EducationFormset(instance=candidate)
    else:
        form = AddCandidateForm()
        testing_formset = TestingFormset()
        education_formset = EducationFormset()
    if request.method == "POST":
        form = AddCandidateForm(request.POST, request.FILES)
        testing_formset = TestingFormset(request.POST, instance=candidate)
        education_formset = EducationFormset(request.POST, instance=candidate)
        if form.is_valid() and testing_formset.is_valid() and education_formset.is_valid():
            form.save()
            testing_formset.save()
            education_formset.save()
            return redirect('dashboard')
    context = {
        'form':form,
        'testing_formset':testing_formset,
        'education_formset':education_formset}
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
    dept_members = staff_list.filter(position = ADMISSION_DEPARTMENT)
    committie_members = staff_list.filter(position = COMMITTIE_MEMBER)
    chairs = staff_list.filter(position = COMMITIE_CHAIR)
    secretaries = staff_list.filter(position = SECRETARY)
    context ={
        'dept_members':dept_members,
        'committie':committie_members,
        'chairs':chairs,
        'secretaries':secretaries,
        }
    return render(request, 'mainapp/contacts.html', context)

@login_required(login_url = 'login')
def personalView(request):
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
        'position':POSITIONS[request.user.position],
        'form': form,
        'user':request.user
        }
    return render(request, 'mainapp/personal.html', context)


@login_required(login_url = 'login')
def profileView(request, uuid):
    if uuid.replace(" ", "")==str(request.user.staff_id):
        return redirect('personal')
    context ={
        'position':POSITIONS[request.user.position],
        'user': get_object_or_404(get_user_model(), staff_id=uuid)
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
@check_permissions(allowed_pos=[COMMITIE_CHAIR])
def ChairView(request):
    admission_year, admission_round = getCurrentAdmissionsYearAndRound()

    try:
        candidates = admission_round.candidatemodel_set.all()
        evaluated_candidates_count = len(candidates.filter(evaluation_finished=True))
        non_evaluated_candidates_count = len(candidates.exclude(evaluation_finished=True))
    except (ObjectDoesNotExist, AttributeError):
        return redirect('dashboard')
    form = AdmissionRoundForm()
    context = {
        'form':form,
        'candidates':candidates,
        'total_candidates':len(candidates),
        'evaluated_candidates_count':evaluated_candidates_count,
        'non_evaluated_candidates_count':non_evaluated_candidates_count
      }
    if request.method == "POST":
        form = AdmissionRoundForm(request.POST, instance = admission_round)
        if non_evaluated_candidates_count!=0:
            messages.error(request,'Evaluation of candidates is not finished yet')
            return render(request, 'mainapp/chair_template.html', context) 
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    return render(request, 'mainapp/chair_template.html', context)

