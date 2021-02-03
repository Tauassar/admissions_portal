from django.http import HttpResponse
from django.shortcuts import redirect
from .models import ProfileModel

def auth_check(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def check_permissions(allowed_pos=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            profile = ProfileModel.objects.get(user = request.user)
            if (profile.position in allowed_pos) or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator