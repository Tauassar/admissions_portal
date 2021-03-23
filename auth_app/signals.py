from django.contrib.auth import (user_login_failed,
                                 user_logged_out,
                                 user_logged_in)
from django.dispatch import receiver

from auth_app.models import AuditEntry


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='Logged in',
                              ip=ip,
                              email=user.email)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='Logged out',
                              ip=ip,
                              email=user.email)


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, request, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='Login failed',
                              email=credentials.get('username', None),
                              ip=ip)
