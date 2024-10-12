from django import forms
from django.forms import ModelForm
from .models import *
from models import Pet
from django.contrib.auth.models import User
from django.forms.widgets import DateInput

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password','first_name', 'last_name')
        help_texts = {
        'username': None,  
        }
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 4: 
            raise forms.ValidationError("Username must be at least 4 characters long.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:  
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        cleaned_data = super().clean()
        if not cleaned_data.get('email'):
            self.add_error('email', 'This field is required.')
        return email
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ('usertype',)


class ProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class CourseEnrollmentForm(forms.ModelForm):
    class Meta:
        model = CourseEnrollment
        fields = ('courseid',)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = CourseFeedback
        fields = ('feedback',)

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('coursename','coursecode', 'coursestartdate', 'courseenddate')

        widgets = {
            'coursestartdate': DateInput(attrs={'type': 'date'}),
            'courseenddate': DateInput(attrs={'type': 'date'}),
        }

    def clean_coursename(self):
        coursename = self.cleaned_data['coursename']
        if len(coursename) > 30:
            raise forms.ValidationError("Coursename must be at most 30 characters long.")
        if Course.objects.filter(coursename=coursename).exists():
            raise forms.ValidationError("Course with this name already exists.")
        return coursename

    def clean_coursecode(self):
        coursecode = self.cleaned_data['coursecode']
        if len(coursecode) != 4:
            raise forms.ValidationError("Coursecode must be 4 characters long.")
        if Course.objects.filter(coursecode=coursecode).exists():
            raise forms.ValidationError("Course with this Course code already exists.")
        return coursecode

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('coursestartdate')
        end_date = cleaned_data.get('courseenddate')

        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("Start date cannot be after end date.")
        return cleaned_data

    
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True


class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = StatusUpdate
        fields = ['status']

    def clean(self):
        data = self.cleaned_data
        if data.get('status', None):
            return data
        else:
            raise forms.ValidationError('Provide either a date and time or a timestamp')

class FileUpload(forms.ModelForm):
    class Meta:
        model = Fileupload
        fields = ['filename', 'files','courseid']

    def clean_filename(self):
        filename = self.cleaned_data.get('filename')
        if len(filename) >= 20: 
            raise forms.ValidationError("Filename must be less than 20 characters.")
        return filename

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

