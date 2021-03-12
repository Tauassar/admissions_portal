from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import django.contrib.auth

from admission_periods_app.models import AdmissionYearModel
from auth_app.decorators import auth_check
from auth_app.forms import CustomPasswordChangeForm
from auth_app.models import CustomUserModel


@auth_check
def loginView(request):
    context = {}
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = django.contrib.auth.authenticate(
            request, email=email, password=password)

        if user is not None:
            django.contrib.auth.login(request, user)
            return redirect('dashboard')

        else:
            messages.error(request, "Please check username and password")
            return render(request, 'auth_app/login.html', context)

    return render(request, 'auth_app/login.html', context)


def logoutView(request):
    django.contrib.auth.logout(request)
    return redirect('login')


# show staff profiles


@login_required(login_url='login')
def contactsView(request):
    admission_year = get_object_or_404(AdmissionYearModel, active=True)
    staff_list = admission_year.get_staff_list()
    dept_members = staff_list.filter(
        position=CustomUserModel.ADMISSION_DEPARTMENT)
    committee_members = staff_list.filter(
        position=CustomUserModel.COMMITTEE_MEMBER)
    chairs = staff_list.filter(position=CustomUserModel.COMMITTEE_CHAIR)
    secretaries = staff_list.filter(position=CustomUserModel.SECRETARY)
    context = {
        'dept_members': dept_members,
        'committee': committee_members,
        'chairs': chairs,
        'secretaries': secretaries,
    }
    return render(request, 'auth_app/contacts.html', context)


@login_required(login_url='login')
def personalView(request):
    if request.method == 'POST':
        print("\n\n\nPOST INIT")
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            print("\n\n\nPass changed")
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('personal')
        else:
            print("\n\n\nError")
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {
        'position': CustomUserModel.POSITIONS[request.user.position][1],
        'form': form,
        'user': request.user
    }
    return render(request, 'auth_app/personal.html', context)


@login_required(login_url='login')
def profileView(request, uuid):
    if uuid.replace(" ", "") == str(request.user.staff_id):
        return redirect('personal')
    context = {
        'position': CustomUserModel.POSITIONS[request.user.position][1],
        'user': get_object_or_404(get_user_model(), staff_id=uuid)
    }
    return render(request, 'auth_app/personal.html', context)
