from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from projectsite.models import College, Program, Student, Organization, Orgmembers
import random

class Command(BaseCommand):
    help = 'Creates initial data for testing'

    def __init__(self):
        super().__init__()
        self.fake = Faker()

    def handle(self, *args, **kwargs):
        self.create_colleges()
        self.create_organizations()
        self.create_programs()
        self.create_students(50)
        self.create_orgmembers()

    def create_colleges(self):
        colleges = [
            "College of Engineering",
            "College of Business",
            "College of Arts and Sciences",
            "College of Education"
        ]
        for name in colleges:
            College.objects.get_or_create(college_name=name)
        self.stdout.write(self.style.SUCCESS('Created colleges'))

    def create_organizations(self):
        orgs = [
            "Student Council",
            "Engineering Society",
            "Business Club",
            "Arts Club",
            "Science Club"
        ]
        for name in orgs:
            Organization.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS('Created organizations'))

    def create_programs(self):
        programs = {
            "College of Engineering": ["Computer Engineering", "Civil Engineering", "Electrical Engineering"],
            "College of Business": ["Business Administration", "Accountancy", "Economics"],
            "College of Arts and Sciences": ["Psychology", "Biology", "Chemistry"],
            "College of Education": ["Elementary Education", "Secondary Education"]
        }
        
        for college_name, program_list in programs.items():
            college = College.objects.get(college_name=college_name)
            for program_name in program_list:
                Program.objects.get_or_create(program_name=program_name, college=college)
        self.stdout.write(self.style.SUCCESS('Created programs'))

    def create_students(self, count):
        programs = list(Program.objects.all())
        for _ in range(count):
            student = Student.objects.create(
                student_id=f"2024{self.fake.unique.random_number(digits=4)}",
                first_name=self.fake.first_name(),
                last_name=self.fake.last_name(),
                middle_name=self.fake.last_name() if random.choice([True, False]) else None,
                program=random.choice(programs)
            )
        self.stdout.write(self.style.SUCCESS(f'Created {count} students'))

    def create_orgmembers(self):
        students = list(Student.objects.all())
        organizations = list(Organization.objects.all())
        
        for student in students:
            # Randomly assign 1-3 organizations to each student
            for org in random.sample(organizations, random.randint(1, 3)):
                Orgmembers.objects.create(
                    student=student,
                    organization=org,
                    date_joined=self.fake.date_between(start_date='-2y', end_date='today')
                )
        self.stdout.write(self.style.SUCCESS('Created organization memberships'))