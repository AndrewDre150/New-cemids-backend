from django.db import models

# profiles/models.py

from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    nationality = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    job_title = models.CharField(max_length=100)
    email = models.EmailField()
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    def __str__(self):
        return f'{self.name} {self.surname}'

