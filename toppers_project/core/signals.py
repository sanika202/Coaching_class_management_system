from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import CustomUser, StudentProfile, TeacherProfile, Notification


@receiver(post_save, sender=CustomUser)
def create_notification_on_registration(sender, instance, created, **kwargs):
    """Create notification when new user registers"""
    if created and instance.role != 'admin':
        admin_user = CustomUser.objects.filter(role='admin').first()
        if admin_user:
            Notification.objects.create(
                user=admin_user,
                notification_type='registration',
                title=f'New {instance.get_role_display()} Registration',
                message=f'{instance.get_full_name()} ({instance.username}) has registered as {instance.get_role_display()}',
                related_user=instance
            )
