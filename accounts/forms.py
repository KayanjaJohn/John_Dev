from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django import forms
from .models import CustomUserRegistration
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import re
from .models import (
    CustomUserRegistration, 
    DepartmentalObjective, 
    StrategicResult, 
    PerformanceMeasure, 
    Target,
    DepartmentalInitiativeOrActivities, 
    Deliverable,
    Formula,
    PerformanceMeasureActualResults,
    ActualExpenditure,
    InitialTemplateDetail,
    AchievementChallenge,
)

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['email'].required = False
        self.fields['department'].required = False
        # self.fields['disconnect_date'].required = False
        self.fields['password1'].required = False
        self.fields['password2'].required = False

class RegistrationForm(CustomUserCreationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id':'username',  'autocomplete': 'off', 'placeholder': 'Enter  username'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id':'first_name',  'autocomplete': 'off', 'placeholder': 'Enter  first name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id':'last_name',  'autocomplete': 'off', 'placeholder': 'Enter  last name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'id':'email',  'autocomplete': 'off', 'placeholder': 'Enter  email'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'id':'password1',  'autocomplete': 'off', 'placeholder': 'Enter  password'}))
    password2 = forms.CharField(label="Comfirm password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'id':'password2',  'autocomplete': 'off', 'placeholder': 'Confirm  password'}))

    is_strategy = forms.BooleanField(required=False)
    is_admin = forms.BooleanField(required=False)
    is_work_plan_manager = forms.BooleanField(required=False)
    is_manager = forms.BooleanField(required=False)
    is_director = forms.BooleanField(required=False)

    #Registration comfirmation email
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

            full_name = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
            username = f"{self.cleaned_data['username']}"
            password = f"{self.cleaned_data['password1']}"
            subject = 'You are welcome to the BOU PAR AUTOMATION SYSTEM.'
            message = f'Dear {full_name}, you now have access to our system.\n Your username is: {username}. \n Your system password is: {password}.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [self.cleaned_data['email']]
            send_mail(subject, message, from_email, recipient_list)
        
        return user

    #Email Validation
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if CustomUserRegistration.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists. Please choose a different email.")

        if not email:
            raise forms.ValidationError("Email is required. Please provide a email.")

        return email

    #Username Validation
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if CustomUserRegistration.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists. Please choose a different username.")

        if not username:
            raise forms.ValidationError("Username is required. Please provide a username.")

        if not re.match(r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*@)[a-zA-Z\d@]+$", username):
            raise forms.ValidationError("Username must contain a mix of letters, numbers, '@' and no spaces.")

        if len(username) < 4 or len(username) > 150:
            raise forms.ValidationError("Username must be between 4 and 150 characters.")

        return username



    class Meta(UserCreationForm):
        model = CustomUserRegistration
        fields = UserCreationForm.Meta.fields + ('username', 'first_name', 'last_name', 'email','department', 'is_strategy', 'is_admin', 'is_director', 'is_work_plan_manager', 'is_manager', 'disconnect_date')
        widgets = {
            'department': forms.Select(attrs={'class': 'department', 'id': 'department'}),
            'disconnect_date': forms.DateInput(attrs={'class': 'form-control', 'id':'disconnect_date', 'type': 'date'})
        }

#UPDATE FORM
class UpdateForm(forms.ModelForm):
    is_strategy = forms.BooleanField(required=False)
    is_admin = forms.BooleanField(required=False)
    is_work_plan_manager = forms.BooleanField(required=False)
    is_manager = forms.BooleanField(required=False)
    is_director = forms.BooleanField(required=False)
    class Meta:
        model = CustomUserRegistration
        fields = ['username', 'first_name', 'last_name', 'email', 'department', 'is_strategy', 'is_admin', 'is_director', 'is_work_plan_manager', 'is_manager', 'disconnect_date']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'department'}),
            'disconnect_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUserRegistration
        fields = UserChangeForm.Meta.fields

class DepartmentalObjectiveForm(ModelForm):
    class Meta:
        model = DepartmentalObjective
        fields = ['departmental_objective','corporate_strategic_initiative']

class StrategicResultForm(ModelForm):
    class Meta:
        model = StrategicResult
        fields = ['strategic_result']

class PerformanceMeasureForm(ModelForm):
    class Meta:
        model = PerformanceMeasure
        fields = ['performance_measure', 'performance_measure_target']

class TargetsForm(ModelForm):
    class Meta:
        model = Target
        fields = ['targets_quarterly_annual']

class DepartmentalInitiativeOrActivitiesForm(ModelForm):
    class Meta:
        model = DepartmentalInitiativeOrActivities
        fields = ['departmental_Initiative', 'DPI_CSI_BAU', 'budget_allocation']

class DeliverableForm(ModelForm):
    class Meta:
        model = Deliverable
        fields = ['deliverable', 'start_date', 'end_date',]

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class FormulaForm(ModelForm):
    class Meta:
        model = Formula
        fields = ['formula', 'performance_measure_actual_results']

class PerformanceMeasureActualResultsForm(ModelForm):
    class Meta:
        model = PerformanceMeasureActualResults
        fields = ['performance_measure_actual_results']

class ActualExpenditureForm(ModelForm):
    class Meta:
        model = ActualExpenditure
        fields = ['actual_expenditure']

class InitialTemplateDetailForm(ModelForm):
    class Meta:
        model = InitialTemplateDetail
        fields = ['template_Name', 'financial_Year_Starts', 'financial_Year_Ends']

        widgets = {
            'financial_Year_Starts': forms.DateInput(attrs={'type': 'date'}),
            'financial_Year_Ends': forms.DateInput(attrs={'type': 'date'}),
            'acceptance_Date': forms.DateInput(attrs={'type': 'date'}),
        }

class ManagerDirectorTemplateForm(ModelForm):
    # SELECT_STATUS = [
    #     ('selected', 'Select Template Status'),
    #     ('in progress', 'In Progress'),
    #     ('done', 'Done'),
    # ]
    # template_Status = forms.CharField(widget=forms.Select(choices=SELECT_STATUS, attrs={'class': 'form-control'}))
    class Meta:
        model = InitialTemplateDetail
        fields = []

class AchievementChallengeForm(ModelForm):
    class Meta:
        model = AchievementChallenge
        fields = ['achievement', 'challenge']
