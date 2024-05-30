from django.db import models

# Create your models here.



from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Admin'),
        (2, 'Supervisor'),
        (3, 'Project Coordinator'),
        (4, 'Student'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=4)

class category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name

class Thesis(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    supervisor = models.ForeignKey(User, limit_choices_to={'user_type': 2}, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    students = models.ManyToManyField(User, related_name='theses', limit_choices_to={'user_type': 4}, blank=True, null=True)
    interested = models.ManyToManyField(User, related_name='interested_theses', limit_choices_to={'user_type': 4},blank=True, null=True)

    category = models.ManyToManyField(category, blank=True, null=True)

    software_engineering = models.BooleanField(null=True, blank=True, default=False)
    Information_Systems_and_Data_Science = models.BooleanField(null=True, blank=True, default=False) # Information Systems and Data Science
    Mechanical_Engineering = models.BooleanField(null=True, blank=True, default=False)
    Civil_and_Structural_Engineering = models.BooleanField(null=True, blank=True, default=False)
    Chemical_Engineering = models.BooleanField(null=True, blank=True, default=False)
    External = models.BooleanField(null=True, blank=True, default=False)
    Internal_Sydney = models.BooleanField(null=True, blank=True, default=False)
    Internal_Casuarina = models.BooleanField(null=True, blank=True, default=False) # Internal - Casuarina
    





    def __str__(self):
        return self.title

class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, limit_choices_to={'user_type': 4})
    thesis = models.ForeignKey(Thesis, on_delete=models.CASCADE, limit_choices_to={'is_approved': True})


    def __str__(self):
        return self.name
