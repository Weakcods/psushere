from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class College(BaseModel):
    college_name = models.CharField(max_length=100)

    def __str__(self):
        return self.college_name

class Organization(BaseModel):
    name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name

class Program(BaseModel):
    program_name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.program_name

class Student(BaseModel):
    student_id = models.CharField(max_length=50, unique=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.lastname}, {self.firstname}"

class Orgmembers(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student} - {self.organization}"
