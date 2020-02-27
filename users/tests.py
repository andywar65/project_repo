from django.test import TestCase
from .models import (CourseSchedule, )

class CourseScheduleTestCase(TestCase):
    def setUp(self):
        CourseSchedule.objects.create(full="Lunedì 16:00", abbrev="1-LU16")

    def test_name(self):
        """Name is correctly identified"""
        orario = CourseSchedule.objects.get(abbrev="1-LU16")
        self.assertEqual(orario.__str__(), 'Lunedì 16:00')
