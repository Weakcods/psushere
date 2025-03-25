from django.core.management.base import BaseCommand
from core.models import College, Program, Organization, Student, OrgMember
from faker import Faker
from datetime import date
import random

fake = Faker('en_PH')  # Use Philippines locale

class Command(BaseCommand):
    help = 'Create initial data for the student organization database'

    def handle(self, *args, **kwargs):
        # Create 8 Colleges
        colleges_data = [
            ('College of Computing Studies', 'CCS'),
            ('College of Business Administration', 'CBA'),
            ('College of Arts and Sciences', 'CAS'),
            ('College of Education', 'COE'),
            ('College of Engineering', 'COEng'),
            ('College of Architecture', 'CA'),
            ('College of Nursing', 'CON'),
            ('College of Medicine', 'COM')
        ]
        
        colleges = []
        for name, code in colleges_data:
            college = College.objects.create(
                name=name
            )
            colleges.append(college)
            self.stdout.write(f'Created college: {name}')

        # Create 10 Programs
        programs_data = [
            ('Bachelor of Science in Computer Science', 0),
            ('Bachelor of Science in Information Technology', 0),
            ('Bachelor of Science in Business Administration', 1),
            ('Bachelor of Arts in Psychology', 2),
            ('Bachelor of Science in Education', 3),
            ('Bachelor of Science in Civil Engineering', 4),
            ('Bachelor of Science in Architecture', 5),
            ('Bachelor of Science in Nursing', 6),
            ('Doctor of Medicine', 7),
            ('Bachelor of Science in Accountancy', 1)
        ]

        programs = []
        for name, college_index in programs_data:
            program = Program.objects.create(
                name=name,
                college=colleges[college_index]
            )
            programs.append(program)
            self.stdout.write(f'Created program: {name}')

        # Create 2 Organizations
        orgs = [
            Organization.objects.create(
                name='Association of Computing Students',
                description='Premier organization for computing students',
                college=colleges[0]
            ),
            Organization.objects.create(
                name='Society of Information Technology Enthusiasts',
                description='Promoting excellence in IT education',
                college=colleges[0]
            )
        ]
        self.stdout.write('Created organizations')

        # Create 2 Students
        students = []
        for i in range(2):
            student = Student.objects.create(
                student_id=f'2024-{fake.unique.random_number(digits=4)}',
                lastname=fake.last_name(),
                firstname=fake.first_name(),
                middlename=fake.last_name(),
                program=random.choice(programs[:2])  # Only CS or IT programs
            )
            students.append(student)
            self.stdout.write(f'Created student: {student}')

        # Create 2 OrgMemberships
        positions = ['President', 'Secretary', 'Treasurer', 'Member']
        for i, student in enumerate(students):
            OrgMember.objects.create(
                student=student,
                organization=orgs[i]
            )
            self.stdout.write(f'Created org membership for: {student}')

        self.stdout.write(self.style.SUCCESS('Successfully created initial data'))