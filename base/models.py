from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
import os

GENDER_CHOICES = [
  ('Male', 'Male'),
  ('Female', 'Female'),
]

BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

JOB_CATEGORY_CHOICES = [
    ('Government', 'Government'),
    ('Private', 'Private'),
    ('Bussiness', 'Bussiness'),
    ('Homemaker', 'Homemaker'),
    ('Others', 'Others'),
]

DEPARTMENT_CHOICES = [
  ('Civil Eng.', 'Civil Eng.'),
  ('Architectural Eng.', 'Architectural Eng.'),
  ('Environmental Eng.', 'Environmental Eng.'),
  ('Mechanical Eng.', 'Mechanical Eng.'),
  ('Chemical Eng.', 'Chemical Eng.'),
  ('Food Eng.', 'Food Eng.'),
  ('Electrical Eng.', 'Electrical Eng.'),
  ('Electronics Eng.', 'Electronics Eng.'),
  ('Computer Eng.', 'Computer Eng.'),
  ('Power Eng.', 'Power Eng.'),
  ('Automobile Eng.', 'Automobile Eng.'),
  ('RAC Eng.', 'RAC Eng.'),
]
 
class User(AbstractUser):
  name = models.CharField(max_length=200, null=True)
  email = models.EmailField(unique=True)
  profile_bio = models.TextField(null=True)
  date_of_birth = models.DateField(null=True)
  updated = models.DateTimeField(auto_now=True, null=True)
  current_address = models.TextField(null=True, blank=True)
  permanent_address = models.TextField(null=True, blank=True)

  resume = models.FileField(upload_to='pdfs/', null=True, blank=True) # Stores PDF files in the 'pdfs/' subdirectory of MEDIA_ROOT

  gender = models.CharField(
    max_length=6,
    choices=GENDER_CHOICES,
    null=True,
  )
  blood_group = models.CharField(
      max_length=3,
      choices=BLOOD_GROUP_CHOICES,
      null=True,
  )

  department = models.CharField(
      max_length=18,
      choices=DEPARTMENT_CHOICES,
      null=True,
  )

  job_type = models.CharField(max_length=10, choices=JOB_CATEGORY_CHOICES, null=True, blank=True)
  job_role = models.CharField(max_length=100, null=True, blank=True)
  job_description = models.TextField(null=True, blank=True)


  avatar = models.ImageField(upload_to='images/', null=True, blank=True)

  # to use user.date_joined;

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  def __str__(self):
    return self.email

  def has_complete_profile(self):
    return self.name and self.profile_bio and self.date_of_birth and self.gender and self.blood_group



class ContactInfo(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
  type = models.CharField(max_length=50)
  value = models.CharField(max_length=255)

  def __str__(self):
    return f"{self.type}: {self.value}"
  

class Registration(models.Model):
  email = models.EmailField(null=True)
  otp = models.CharField(max_length=6, null=True)
  created_at = models.DateTimeField(auto_now=True)
  registrationKey = models.CharField(max_length=8)
  is_used = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.email} - {self.otp}"
    




@receiver(pre_save, sender=User)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # New object, no old file to delete

    try:
        old_instance = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return

    # Check image change
    if old_instance.avatar and old_instance.avatar != instance.avatar:
        if os.path.isfile(old_instance.avatar.path):
            os.remove(old_instance.avatar.path)

    # Check resume change
    if old_instance.resume and old_instance.resume != instance.resume:
        if os.path.isfile(old_instance.resume.path):
            os.remove(old_instance.resume.path)


# 🔹 Delete files when object is deleted
@receiver(post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.avatar and os.path.isfile(instance.avatar.path):
        os.remove(instance.avatar.path)

    if instance.resume and os.path.isfile(instance.resume.path):
        os.remove(instance.resume.path)