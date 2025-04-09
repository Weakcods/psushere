from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from projectsite.models import College, Program, Student, Organization, Orgmembers
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generate fake data for testing'

    def __init__(self):
        super().__init__()
        self.fake = Faker()

    def handle(self, *args, **kwargs):
        # Create Colleges
        colleges = ['College of Engineering', 'College of Science', 'College of Arts', 'College of Business']
        college_objects = []
        for college_name in colleges:
            college = College.objects.create(college_name=college_name)
            college_objects.append(college)

        # Create Programs
        programs = ['Computer Science', 'Civil Engineering', 'Business Administration', 'Psychology']
        program_objects = []
        for program_name in programs:
            program = Program.objects.create(
                program_name=program_name,
                college=random.choice(college_objects)
            )
            program_objects.append(program)

        # Create Organizations
        org_objects = []
        for _ in range(15):
            org = Organization.objects.create(
                name=self.fake.company(),
                college=random.choice(college_objects),
                description=self.fake.text(max_nb_chars=200)
            )
            org_objects.append(org)

        # Create Students
        student_objects = []
        for _ in range(50):
            student = Student.objects.create(
                student_id=f"2024{self.fake.unique.random_number(digits=4)}",
                firstname=self.fake.first_name(),
                lastname=self.fake.last_name(),
                middlename=self.fake.last_name() if random.choice([True, False]) else None,
                program=random.choice(program_objects)
            )
            student_objects.append(student)

        # Create Organization Members
        for student in student_objects:
            # Assign each student to 1-3 random organizations
            for org in random.sample(org_objects, random.randint(1, 3)):
                Orgmembers.objects.create(
                    student=student,
                    organization=org,
                    date_joined=timezone.now() - timedelta(days=random.randint(1, 365))
                )

        self.stdout.write(self.style.SUCCESS('Successfully created fake data'))
