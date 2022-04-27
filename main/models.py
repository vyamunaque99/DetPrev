from importlib.machinery import ModuleSpec
import json

from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
from django.dispatch import receiver
from django_celery_beat.models import IntervalSchedule,PeriodicTask
from django_enum_choices.fields import EnumChoiceField
from django.db.models.signals import post_save
from django.utils import timezone
from .enums import SetupStatus

# Create your models here.
class Dataset(models.Model):
    name=models.CharField(max_length=30,unique=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

class ConformanceChecking(models.Model):
    start_date=models.DateField()
    start_time=models.TimeField()
    process=models.ForeignKey(Dataset,on_delete=models.CASCADE)
    frecuency_time=models.IntegerField()
    frecuency= models.CharField(max_length=7)
    os_user= models.CharField(max_length=30)
    user_ip= models.GenericIPAddressField()
    log_file=models.CharField(max_length=300)
    port_number=models.IntegerField()
    ssh_pub_key=models.CharField(max_length=2000)
    status=EnumChoiceField(SetupStatus,default=SetupStatus.active)
    task=models.OneToOneField(PeriodicTask,on_delete=models.CASCADE,null=True,blank=True)
    def setup_task(self):
        frecuency_interval=IntervalSchedule()
        if self.frecuency=='Minutos':
            frecuency_interval=IntervalSchedule.MINUTES
        elif self.frecuency=='Horas':
            frecuency_interval=IntervalSchedule.HOURS
        elif self.frecuency=='Dias':
            frecuency_interval=IntervalSchedule.DAYS
        IntervalSchedule.objects.get_or_create(every=self.frecuency_time,period=frecuency_interval)
        self.task=PeriodicTask.objects.create(
            name='ConformanceCheking{0}'.format(self.id),
            task='conformance_cheking_task',
            interval= IntervalSchedule.objects.get(every=self.frecuency_time,period=frecuency_interval),
            args=json.dumps([self.id]),
            start_time=timezone.now()
        )
        self.save()

class Stakeholder(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    def __str__(self):
        return u'{0}'.format(self.name)

class StakeholderList(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return u'{0}'.format(self.name)

class StakeholderListDetail(models.Model):
    list_name=models.ForeignKey(StakeholderList,on_delete=models.CASCADE)
    stakeholder_name=models.ForeignKey(Stakeholder,on_delete=models.CASCADE)

@receiver(post_save,sender=ConformanceChecking)
def periodic_task_creation(sender,instance,created,**kwargs):
    if created:
        instance.setup_task()
    else:
        if instance is not None:
            instance.task.enabled=instance.status==SetupStatus.active
            instance.task.save()

