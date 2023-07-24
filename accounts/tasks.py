from accounts.models import CustomUserRegistration

def update_user_status(user_id):
    user = CustomUserRegistration.objects.get(id=user_id)
    user.status = 'Blocked'
    user.save()
