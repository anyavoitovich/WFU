
from django.contrib import admin
from .models import User, Employer, JobSeeker, Vacancy, Resume, ResumeApplication, VacancyApplication, Message, EducationalInstitution, Education, JobCategory

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('UserID', 'first_name', 'last_name', 'email', 'role', 'username')

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('EmployerID', 'company_name')

@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('JobSeekerID', 'birthdate')

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('VacancyID', 'employer', 'title', 'salary')

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('ResumeID', 'job_seeker', 'profession')

@admin.register(ResumeApplication)
class ResumeApplicationAdmin(admin.ModelAdmin):
    list_display = ('ApplicationID', 'resume', 'sender', 'status')

@admin.register(VacancyApplication)
class VacancyApplicationAdmin(admin.ModelAdmin):
    list_display = ('ApplicationID', 'vacancy', 'sender', 'status')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('MessageID', 'sender', 'receiver', 'text', 'timestamp')

@admin.register(EducationalInstitution)
class EducationalInstitutionAdmin(admin.ModelAdmin):
    list_display = ('EduInstitutionID', 'name', 'specialization')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('EducationID', 'resume', 'edu_institution', 'level', 'graduation_year')

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('CategoryID', 'name')

