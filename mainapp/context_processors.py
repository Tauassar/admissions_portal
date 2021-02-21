from .models import ProfileModel

def add_variable_to_context(request):
    return {
        'position': ProfileModel.objects.get(user=request.user).position
    }