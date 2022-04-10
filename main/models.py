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

@receiver(post_save,sender=ConformanceChecking)
def periodic_task_creation(sender,instance,created,**kwargs):
    if created:
        instance.setup_task()
    else:
        if instance is not None:
            instance.task.enabled=instance.status==SetupStatus.active
            instance.task.save()

'''
class Setup(models.Model):
    class Meta:
        verbose_name='Setup'
        verbose_name_plural='Setups'
    class TimeInterval(models.TextChoices):
        one_min = '1 min', _('1 min')
        five_mins = '5 mins', _('5 mins')
        one_hour = '1 hour', _('1 hour')
    class SetupStatus(models.TextChoices):
        active = 'Active', _('Active')
        disabled = 'Disabled', _('Disabled')
    title=models.CharField(max_length=70,blank=False)
    status = ChoiceField(SetupStatus.choices, default=SetupStatus.active)
    created_at = models.DateTimeField(auto_now_add=True)
'''