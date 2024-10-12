from django.test import TestCase
from .forms import UserForm, CourseForm, FileUpload

class UserFormTestCase(TestCase):
    def test_user_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
        }
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_form_invalid(self):

        form_data = {
            'username': 'a',  
            'email': '',       
            'password': '123', 
            'first_name': 'Test',
            'last_name': 'User',
        }
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)  
class CourseFormTestCase(TestCase):
    def test_course_form_valid(self):
        form_data = {
            'coursename': 'Test Course',
            'coursecode': '1234',
            'coursestartdate': '2023-01-01',
            'courseenddate': '2023-02-01',
        }
        form = CourseForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_course_form_invalid(self):
        form_data = {
            'coursename': 'A very long course name exceeding 30 characters limit',
            'coursecode': '123', 
            'coursestartdate': '2023-02-01',
            'courseenddate': '2023-01-01', 
        }
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('coursename', form.errors)
        self.assertIn('coursecode', form.errors)
        self.assertIn('__all__', form.errors)  

class FileUploadFormTestCase(TestCase):
    def test_fileupload_form_valid(self):
        
        file_data = {
            'filename': 'abc',
            'files': None,  
        }
        form = FileUpload(data=file_data)
        self.assertTrue(form.is_valid())

    def test_fileupload_form_invalid(self):
        file_data = {
            'filename': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'files': None,
        }
        form = FileUpload(data=file_data)
        self.assertFalse(form.is_valid())
        self.assertIn('filename', form.errors)

