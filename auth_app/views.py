from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import django.contrib.auth
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from admission_periods_app.models import AdmissionYearModel
from auth_app.decorators import auth_check
from auth_app.forms import CustomPasswordChangeForm, AuthForm
from auth_app.models import CustomUserModel


@auth_check
def loginView(request):
    context = {'form': AuthForm}
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


# show staff profiles


class ContactsView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'auth_app/contacts.html'
    context_object_name = 'users'

    def get_queryset(self):
        admission_year = get_object_or_404(AdmissionYearModel, active=True)
        staff_list = admission_year.get_staff_list()
        dept_members = staff_list.filter(
            position=CustomUserModel.ADMISSION_DEPARTMENT)
        committee_members = staff_list.filter(
            position=CustomUserModel.COMMITTEE_MEMBER)
        chairs = staff_list.filter(position=CustomUserModel.COMMITTEE_CHAIR)
        secretaries = staff_list.filter(position=CustomUserModel.SECRETARY)
        queryset = {
            'dept_members': dept_members,
            'committee': committee_members,
            'chairs': chairs,
            'secretaries': secretaries}
        return queryset


class PersonalView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'auth_app/personal.html'
    success_url = reverse_lazy('personal')
    form_class = CustomPasswordChangeForm

    def get_context_data(self, **kwargs):
        context = super(PasswordChangeView, self).get_context_data(**kwargs)
        context['position'] = CustomUserModel.POSITIONS[
                                  self.request.user.position][1]
        context['user'] = self.request.user
        return context


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'auth_app/personal.html'
    model = get_user_model()
    pk_url_kwarg = 'uuid'
    query_pk_and_slug = 'staff_id'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['position'] = CustomUserModel.POSITIONS[
                                  self.object.position][1]
        context['user'] = self.object
        return context
