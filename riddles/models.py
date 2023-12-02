from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    UserID = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[('Employer', 'Работодатель'), ('JobSeeker', 'Соискатель'), ('Admin', 'Администратор')])

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        # Автоматически установить имя пользователя в значение электронной почты
        self.username = self.email
        super().save(*args, **kwargs)

    def is_employer(self):
        return self.role == 'Employer'

    def is_jobseeker(self):
        return self.role == 'JobSeeker'
class Employer(models.Model):
    EmployerID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=100)
    company_description = models.TextField()
    def __str__(self):
        return f"{self.EmployerID.email}"
class JobSeeker(models.Model):
    JobSeekerID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birthdate = models.DateField()
    education = models.TextField()
    experience = models.TextField()

    def __str__(self):
        return f"{self.JobSeekerID.email}"

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

    def __str__(self):
        return f"{self.profession} - {self.job_seeker.JobSeekerID.email}"
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
    def __str__(self):
        return f"{self.name} - {self.specialization}"
class Education(models.Model):
    EducationID = models.AutoField(primary_key=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    edu_institution = models.ForeignKey(EducationalInstitution, on_delete=models.CASCADE)
    level = models.CharField(max_length=100)
    graduation_year = models.IntegerField()

class JobCategory(models.Model):
    CategoryID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)



