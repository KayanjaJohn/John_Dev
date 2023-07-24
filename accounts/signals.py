from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from accounts.models import CustomUserRegistration
from django_q.tasks import schedule

@receiver(post_save, sender=CustomUserRegistration)
def schedule_status_update(sender, instance, **kwargs):
    current_date = timezone.now().date()
    disconnect_date = instance.disconnect_date

    if disconnect_date and disconnect_date >= current_date:
        # Calculate the number of seconds until the disconnect date
        time_delta = disconnect_date - current_date
        seconds_until_disconnect = time_delta.total_seconds()

        # Schedule the status update task
        schedule('accounts.tasks.update_user_status', instance.id, schedule_type='O', next_run=seconds_until_disconnect)
