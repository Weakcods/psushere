from django.db import models
from django.contrib.auth.models import User

class College(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)  # Added back as it's used in admin
    description = models.TextField()        # Added back as it's used in populate_db

    def __str__(self):
        return self.name

class Program(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)  # Added back as it's used in admin
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Organization(models.Model):
    name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    description = models.TextField()
    

    def __str__(self):
        return self.name

class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True)
    lastname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lastname}, {self.firstname} {self.middlename}"

class OrgMember(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date_joined = models.DateField()
    position = models.CharField(max_length=50)  # Added back as it's used in admin

    def __str__(self):
        return f"{self.student} - {self.organization}"