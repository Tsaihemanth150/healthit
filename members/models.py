from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Plan(models.Model):
    plan_id = models.CharField(max_length=10, unique=True, default='', editable=False)
    name = models.CharField(max_length=25)
    price = models.IntegerField()
    plan_type = models.CharField(max_length=25)
    validity = models.IntegerField(null=True)
    care_staff_available=models.BooleanField(default=False)
    dedicated_services= models.BooleanField(default=False)
    alerts=models.BooleanField(default=False)
    free_pharmacy=models.BooleanField(default=False)
    free_laboratory=models.BooleanField(default=False)
    video_consultation=models.BooleanField(default=False)



    def __str__(self):
        return self.name


@receiver(pre_save, sender=Plan)
def generate_plan_id(sender, instance, **kwargs):
    # Check if the instance is being created for the first time
    if not instance.plan_id:
        # Generate a unique ID in the format HLTDPTXXXX
        last_id = Plan.objects.order_by('-plan_id').first()
        if last_id and last_id.plan_id:  # Check if last_id.custom_id is not empty
            last_id_number = int(last_id.plan_id[6:]) + 1
        else:
            last_id_number = 1
        instance.plan_id = f'HLTPLN{str(last_id_number).zfill(4)}'


class Member(models.Model):
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=500)
    gender = models.CharField(max_length=10, null=True)
    mobile = models.CharField(max_length=20, null=False)
    nationality = models.CharField(max_length=40, null=True)
    custom_id = models.CharField(max_length=8, unique=True, default='', editable=False)  # Set a default value
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL,null=True, related_name='member')


    @property
    def get_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.get_name


@receiver(pre_save, sender=Member)
def generate_member_id(sender, instance, **kwargs):
    # Check if the instance is being created for the first time
    if not instance.custom_id:
        # Generate a unique ID in the format HLTXXXX
        last_id = Member.objects.order_by('-custom_id').first()
        if last_id:
            last_id_number = int(last_id.custom_id[3:]) + 1
        else:
            last_id_number = 1
        instance.custom_id = f'HLT{str(last_id_number).zfill(4)}'


class Question(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    admin_comment = models.CharField(max_length=200, default='Nothing')
    asked_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.description


class Department(models.Model):
    Dept_id = models.CharField(max_length=10, unique=True, default='', editable=False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Department)
def generate_dept_id(sender, instance, **kwargs):
    # Check if the instance is being created for the first time
    if not instance.Dept_id:
        # Generate a unique ID in the format HLTDPTXXXX
        last_id = Department.objects.order_by('-Dept_id').first()
        if last_id and last_id.Dept_id:  # Check if last_id.custom_id is not empty
            last_id_number = int(last_id.Dept_id[6:]) + 1
        else:
            last_id_number = 1
        instance.Dept_id = f'HLTDPT{str(last_id_number).zfill(4)}'
