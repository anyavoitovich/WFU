from django.db import models

class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=[('Employer', 'Работодатель'), ('JobSeeker', 'Соискатель'), ('Admin', 'Admin')])


class Employer(models.Model):
    EmployerID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=100)
    company_description = models.TextField()

class JobSeeker(models.Model):
    JobSeekerID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birthdate = models.DateField()
    education = models.TextField()
    experience = models.TextField()

class Vacancy(models.Model):
    VacancyID = models.AutoField(primary_key=True)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

class Resume(models.Model):
    ResumeID = models.AutoField(primary_key=True)
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100)
    skills = models.TextField()
    experience = models.TextField()

class ResumeApplication(models.Model):
    ApplicationID = models.AutoField(primary_key=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Accepted', 'Принят'), ('Rejected', 'Отклонен'), ('Pending', 'В рассмотрении')])

class VacancyApplication(models.Model):
    ApplicationID = models.AutoField(primary_key=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Accepted', 'Принят'), ('Rejected', 'Отклонен'), ('Pending', 'В рассмотрении')])

class Message(models.Model):
    MessageID = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class EducationalInstitution(models.Model):
    EduInstitutionID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

class Education(models.Model):
    EducationID = models.AutoField(primary_key=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    edu_institution = models.ForeignKey(EducationalInstitution, on_delete=models.CASCADE)
    level = models.CharField(max_length=100)
    graduation_year = models.IntegerField()

class JobCategory(models.Model):
    CategoryID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
# Create your models here.
