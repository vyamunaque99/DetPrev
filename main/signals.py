from turtle import pos
from django.db.models.signals import post_save
from django.dispatch import receiver
from models import ConformanceChecking
from enums import SetupStatus
'''
@receiver(post_save,sender=ConformanceChecking)
def periodic_task_creation(sender,instance,created,**kwargs):
    if created:
        instance.setup_task()
    else:
        if instance is not None:
            instance.task.enabled=instance.status==SetupStatus.active
            instance.task.save()
'''