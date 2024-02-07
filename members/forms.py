from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from members import models


class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['description', 'admin_comment']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6, 'cols': 30})
        }

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['admin_comment'].required = False

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = ['name']


class AssignDepartmentForm(forms.Form):
    department = forms.ModelChoiceField(queryset=models.Department.objects.all(), empty_label="Select department")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PlansForm(forms.ModelForm):
    class Meta:
        model = models.Plan
        fields = ['name', 'price', 'plan_type','validity','care_staff_available','dedicated_services','alerts','free_pharmacy','free_laboratory','video_consultation']


class AssignPlansForm(forms.Form):
    plan = forms.ModelChoiceField(queryset=models.Plan.objects.all(), empty_label="Select Plan")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
