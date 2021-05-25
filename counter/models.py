from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Employee(models.Model):
    E_CHOICE = (('0', 'Online'), ('1', 'Leave'), ('3', 'Resigned'),)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # ! company foreign key is pending to add
    emp_id = models.CharField(
        max_length=50, unique=True, verbose_name="employee id")
    position = models.CharField(max_length=100, verbose_name="job position")
    j_date = models.DateField(verbose_name="joining date")
    status = models.CharField(max_length=10, choices=E_CHOICE, default='1')
    # verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)+" "+self.position


class Service(models.Model):
    # ! company foreign key is pending to add
    name = models.CharField(max_length=200, verbose_name="service name")
    desc = models.TextField(blank=True, null=True, verbose_name="description")
    doc = models.TextField(blank=True, null=True, verbose_name='documents')

    def __str__(self):
        return self.name
