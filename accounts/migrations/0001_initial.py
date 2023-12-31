# Generated by Django 4.2.2 on 2023-07-20 20:37

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUserRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Blocked', 'Blocked')], default='active', max_length=20)),
                ('is_strategy', models.BooleanField(blank=True, default=False, null=True)),
                ('is_admin', models.BooleanField(blank=True, default=False, null=True)),
                ('is_director', models.BooleanField(blank=True, default=False, null=True)),
                ('is_work_plan_manager', models.BooleanField(blank=True, default=False, null=True)),
                ('is_manager', models.BooleanField(blank=True, default=False, null=True)),
                ('disconnect_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(choices=[('Economic Research', 'Economic Research'), ('Communications and Public Relations', 'Communications and Public Relations'), ('Statistics', 'Statistics'), ('Strategy and Innovation', 'Strategy and Innovation'), ('Commercial Bank Supervision', 'Commercial Bank Supervision'), ('Non-Bank FI Supervision', 'Non-Bank FI Supervision'), ('Back Office Operations', 'Back Office Operations'), ('Front Office Operations', 'Front Office Operations'), ('National Payment Systems', 'National Payment Systems'), ('Regional Branches', 'Regional Branches'), ('Domestic Market Operations', 'Domestic Market Operations'), ('Reserves and Investment Management', 'Reserves and Investment Management'), ('Procurement and Disposal', 'Procurement and Disposal'), ('Human Resources', 'Human Resources'), ('Administrative Services', 'Administrative Services'), ('Security Services', 'Security Services'), ('IT Operations and Infrastructure', 'IT Operations and Infrastructure'), ('Business Automation', 'Business Automation'), ('Financial Reporting', 'Financial Reporting'), ('Pension Administration', 'Pension Administration'), ('Medical Services', 'Medical Services'), ('Financial Stability', 'Financial Stability'), ('Risk Management', 'Risk Management')], max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DepartmentalObjective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('financial_year', models.CharField(max_length=256, null=True)),
                ('departmental_objective', models.CharField(max_length=500, null=True)),
                ('corporate_strategic_initiative', models.CharField(blank=True, max_length=500, null=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.department')),
            ],
        ),
        migrations.CreateModel(
            name='Formula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formula', models.CharField(max_length=255)),
                ('performance_measure_actual_results', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PerformanceMeasure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('performance_measure', models.CharField(max_length=500, null=True)),
                ('performance_measure_target', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Perspective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perspective', models.CharField(choices=[('Customer', 'Customer'), ('Finance', 'Finance'), ('Internal Business Processes', 'Internal Business Processes'), ('Organizational Capacity', 'Organizational Capacity')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('targets_quarterly_annual', models.CharField(max_length=500)),
                ('performance_measure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.performancemeasure')),
            ],
        ),
        migrations.CreateModel(
            name='StrategicResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strategic_result', models.CharField(max_length=500)),
                ('departmental_objective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.departmentalobjective')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forget_password_token', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PerformanceMeasureActualResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('performance_measure_actual_results', models.CharField(max_length=255, null=True)),
                ('formula', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.formula')),
            ],
        ),
        migrations.AddField(
            model_name='performancemeasure',
            name='strategic_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.strategicresult'),
        ),
        migrations.CreateModel(
            name='InitialTemplateDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_Name', models.CharField(max_length=255)),
                ('financial_Year_Starts', models.DateField(default=True)),
                ('financial_Year_Ends', models.DateField(default=True)),
                ('template_Status', models.CharField(blank=True, max_length=255, null=True)),
                ('acceptance_Date', models.DateField(blank=True, default=datetime.datetime.now, editable=False)),
                ('user_is_strategy', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.department')),
            ],
        ),
        migrations.AddField(
            model_name='formula',
            name='performance_measure',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.performancemeasure'),
        ),
        migrations.AddField(
            model_name='departmentalobjective',
            name='perspective',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.perspective'),
        ),
        migrations.AddField(
            model_name='departmentalobjective',
            name='template_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.initialtemplatedetail'),
        ),
        migrations.CreateModel(
            name='DepartmentalInitiativeOrActivities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departmental_Initiative', models.CharField(max_length=500)),
                ('DPI_CSI_BAU', models.CharField(choices=[('DPI', 'DPI'), ('CSI', 'CSI'), ('BAU', 'BAU')], max_length=100)),
                ('budget_allocation', models.CharField(max_length=200)),
                ('activity_status', models.CharField(default='Pending', max_length=255, null=True)),
                ('performance_measure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.performancemeasure')),
            ],
        ),
        migrations.CreateModel(
            name='Deliverable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deliverable', models.CharField(max_length=500)),
                ('start_date', models.DateField(default=True)),
                ('end_date', models.DateField(default=True)),
                ('lead_person', models.CharField(blank=True, max_length=255, null=True)),
                ('deliverable_status', models.CharField(default='Pending', max_length=255, null=True)),
                ('departmentalInitiativeOrActivity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.departmentalinitiativeoractivities')),
            ],
        ),
        migrations.CreateModel(
            name='ActualExpenditure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actual_expenditure', models.CharField(max_length=255)),
                ('departmentalInitiativeOrActivity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.departmentalinitiativeoractivities')),
            ],
        ),
        migrations.CreateModel(
            name='AchievementChallenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('achievement', models.CharField(max_length=255, null=True)),
                ('achievement_status', models.CharField(default='Pending', max_length=255)),
                ('challenge', models.CharField(max_length=255, null=True)),
                ('deliverable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.deliverable')),
            ],
        ),
        migrations.AddField(
            model_name='customuserregistration',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.department'),
        ),
        migrations.AddField(
            model_name='customuserregistration',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='customuserregistration',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
