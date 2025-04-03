from django.db import models

class College(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Program(models.Model):
    name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Organization(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    college = models.ForeignKey(College, on_delete=models.CASCADE)  # Add this line

    def __str__(self):
        return self.name

class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True)
    lastname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50)  # Fixed typo in max_length
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lastname}, {self.firstname} {self.middlename}"

class OrgMember(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} - {self.organization}"