from .models import ProfileModel

def add_variable_to_context(request):
    return {
        'user_profile': ProfileModel.objects.get(user=request.user).position,
        'profile_pic': ProfileModel.objects.get(user=request.user).profile_pic
    }