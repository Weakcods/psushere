from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class College(BaseModel):
    college_name = models.CharField(max_length=150)

    def __str__(self):
        return self.college_name

class Organization(BaseModel):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Program(BaseModel):
    program_name = models.CharField(max_length=150)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.program_name

class Student(BaseModel):
    student_id = models.CharField(max_length=15)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=25, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Orgmembers(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date_joined = models.DateField()
    
    
    # 