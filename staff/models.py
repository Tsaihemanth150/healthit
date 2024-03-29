from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from members import models as MMODEL
class Staff(models.Model):
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=500)
    healthit_staff = models.BooleanField(default=True)
    mobile = models.CharField(max_length=20, null=False)
    nationality = models.CharField(max_length=40, null=True)
    custom_id = models.CharField(max_length=8, unique=True, default='', editable=False)  # Set a default value
    department = models.ForeignKey(MMODEL.Department, on_delete=models.SET_NULL, null=True, related_name='staff')
    members = models.ManyToManyField(MMODEL.Member, related_name='staff')
    @property
    def get_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.get_name

@receiver(pre_save, sender=Staff)
def generate_staff_id(sender, instance, **kwargs):
    # Check if the instance is being created for the first time
    if not instance.custom_id:
        # Generate a unique ID in the format HLTSTFXXXX
        last_id = Staff.objects.order_by('-custom_id').first()
        if last_id:
            last_id_number = int(last_id.custom_id[6:]) + 1
        else:
            last_id_number = 1
        instance.custom_id = f'HLTSTF{str(last_id_number).zfill(4)}'

class ScheduleBlock(models.Model):
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='schedule_blocks')
    desc = models.CharField(max_length=50,null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Schedule block for {self.staff.user.username} on {self.date.strftime('%d-%m-%Y')} from {self.start_time.strftime('%H:%M')} to {self.end_time.strftime('%H:%M')}"