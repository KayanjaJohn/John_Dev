from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone
from django.conf import settings

class Department(models.Model):
    DEPARTMENTS = (
        ('Economic Research', 'Economic Research'),
        ('Communications and Public Relations', 'Communications and Public Relations'),
        ('Statistics', 'Statistics'),
        ('Strategy and Innovation', 'Strategy and Innovation'),
        ('Commercial Bank Supervision', 'Commercial Bank Supervision'),
        ('Non-Bank FI Supervision', 'Non-Bank FI Supervision'),
        ('Back Office Operations', 'Back Office Operations'),
        ('Front Office Operations', 'Front Office Operations'),
        ('National Payment Systems', 'National Payment Systems'),
        ('Regional Branches', 'Regional Branches'),
        ('Domestic Market Operations', 'Domestic Market Operations'),
        ('Reserves and Investment Management', 'Reserves and Investment Management'),
        ('Procurement and Disposal', 'Procurement and Disposal'),
        ('Human Resources', 'Human Resources'),
        ('Administrative Services', 'Administrative Services'),
        ('Security Services', 'Security Services'),
        ('IT Operations and Infrastructure', 'IT Operations and Infrastructure'),
        ('Business Automation', 'Business Automation'),
        ('Financial Reporting', 'Financial Reporting'),
        ('Pension Administration', 'Pension Administration'),
        ('Medical Services', 'Medical Services'),
        ('Financial Stability', 'Financial Stability'),
        ('Risk Management', 'Risk Management'),
    )

    department = models.CharField(max_length=100, null=True, choices=DEPARTMENTS)

    def __str__(self):
        return self.department


class CustomUserRegistration(AbstractUser):
    STATUS = (
        ('Active', 'Active'),
        ('Blocked', 'Blocked'),# will set the is_active field of this user to False
    )
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE)#once we have the user role we can then attach the users to any group
    status = models.CharField(max_length=20, null=False, choices=STATUS, default='active')
    is_strategy = models.BooleanField(null=True, blank=True, default=False)
    is_admin = models.BooleanField(null=True, blank=True, default=False)
    is_director = models.BooleanField(null=True, blank=True, default=False)
    is_work_plan_manager = models.BooleanField(null=True, blank=True, default=False)
    is_manager = models.BooleanField(null=True, blank=True, default=False)  
    disconnect_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        current_date = timezone.now().date()
        if self.disconnect_date and self.disconnect_date <= current_date:
            self.status = 'Blocked'
        else:
            self.status = 'Active'
        super().save(*args, **kwargs)

class Perspective(models.Model):
    PERSPECTIVES = (
        ('Customer', 'Customer'),
        ('Finance', 'Finance'),
        ('Internal Business Processes', 'Internal Business Processes'),
        ('Organizational Capacity', 'Organizational Capacity'),
    )

    perspective = models.CharField(max_length=100, null=False, choices=PERSPECTIVES)

    def __str__(self):
        return self.perspective

class InitialTemplateDetail(models.Model):
    template_Name = models.CharField(max_length=255, null=False)
    financial_Year_Starts = models.DateField(default=True)
    financial_Year_Ends = models.DateField(default=True)
    template_Status = models.CharField(max_length=255, null=True, blank=True)
    department = models.ForeignKey(Department, null=True, on_delete=models.CASCADE, blank=True)
    acceptance_Date =models.DateField(editable=False, default=datetime.now, null=False, blank=True)
    created_by = models.ForeignKey(CustomUserRegistration, null=True, on_delete=models.CASCADE)
    user_is_strategy = models.BooleanField(default=False)

    def __str__(self):
        return self.template_Name

class DepartmentalObjective(models.Model):
    perspective = models.ForeignKey(Perspective, null=False, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True, on_delete=models.CASCADE)
    template_name = models.ForeignKey(InitialTemplateDetail,null=True, on_delete=models.CASCADE)
    financial_year = models.CharField(max_length=256, null=True)
    departmental_objective = models.CharField(max_length=500, null=True)
    corporate_strategic_initiative = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.departmental_objective
    
class StrategicResult(models.Model):
    departmental_objective = models.ForeignKey(DepartmentalObjective, null=False, on_delete=models.CASCADE)
    strategic_result = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.strategic_result
    
class PerformanceMeasure(models.Model):
    strategic_result = models.ForeignKey(StrategicResult, null=False, on_delete=models.CASCADE)
    performance_measure = models.CharField(max_length=500, null=True)
    performance_measure_target = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.performance_measure
    
class Target(models.Model):
    performance_measure = models.ForeignKey(PerformanceMeasure, null=False, on_delete=models.CASCADE)
    targets_quarterly_annual = models.CharField(max_length=500)

    def __str__(self):
        return self.targets_quarterly_annual
    
class DepartmentalInitiativeOrActivities(models.Model):
    ACTIVITY_TYPE = (
        ('DPI','DPI'),
        ('CSI','CSI'),
        ('BAU','BAU'),
    )

    performance_measure = models.ForeignKey(PerformanceMeasure, null=False, on_delete=models.CASCADE)
    departmental_Initiative = models.CharField(max_length=500)
    DPI_CSI_BAU = models.CharField(max_length=100, null=False, choices=ACTIVITY_TYPE)
    budget_allocation = models.CharField(max_length=200)
    activity_status = models.CharField(max_length=255, null=True, default='Pending')

    def __str__(self):
        return self.departmental_Initiative

class Deliverable(models.Model):
    departmentalInitiativeOrActivity = models.ForeignKey(DepartmentalInitiativeOrActivities, null=False, on_delete=models.CASCADE)
    deliverable = models.CharField(max_length=500)
    start_date = models.DateField(default=True)
    end_date = models.DateField(default=True)
    lead_person = models.CharField(max_length=255, null=True, blank=True)
    deliverable_status = models.CharField(max_length=255, null=True, default='Pending')

    def __str__(self):
        return self.deliverable
    
class Formula(models.Model):
    performance_measure = models.ForeignKey(PerformanceMeasure, null=True, on_delete=models.CASCADE)
    formula = models.CharField(max_length=255)
    performance_measure_actual_results = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.formula

class PerformanceMeasureActualResults(models.Model):
    formula = models.ForeignKey(Formula, null=True, on_delete=models.CASCADE)
    performance_measure_actual_results = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.performance_measure_actual_results

class ActualExpenditure(models.Model):
    departmentalInitiativeOrActivity = models.ForeignKey(DepartmentalInitiativeOrActivities, null=False, on_delete=models.CASCADE)
    actual_expenditure = models.CharField(max_length=255)

    def __str__(self):
        return str(self.actual_expenditure)


class AchievementChallenge(models.Model):
    deliverable = models.ForeignKey(Deliverable, null=False, on_delete=models.CASCADE)
    achievement = models.CharField(max_length=255, null=True)
    achievement_status = models.CharField(max_length=255, null=False, default='Pending')
    challenge = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.achievement


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username