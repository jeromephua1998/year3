from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

class Student(models.Model):
    studentid = models.AutoField(primary_key=True)
    studentemail = models.EmailField(unique=True)
    studentFirstName = models.CharField(max_length=100,default='John')
    studentLastName = models.CharField(max_length=100,default='Doe')

    def __str__(self):
        return self.studentemail

class Teacher(models.Model):
    teacherid = models.AutoField(primary_key=True)
    teacheremail = models.EmailField(unique=True)
    teacherFirstName = models.CharField(max_length=100,default='John')
    teacherLastName = models.CharField(max_length=100, default='Doe')

    def __str__(self):
        return self.teacheremail

class Course(models.Model):
    courseid = models.AutoField(primary_key=True)
    coursecode = models.CharField(max_length=4)
    coursename = models.CharField(max_length=100)
    coursestartdate = models.DateField()
    courseenddate = models.DateField()
    teacherid = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.coursename

class CourseFeedback(models.Model):
    studentid = models.ForeignKey(Student, on_delete=models.CASCADE)
    courseid = models.ForeignKey(Course, on_delete=models.CASCADE)
    feedback = models.TextField(max_length=200)

class CourseEnrollment(models.Model):
    studentid = models.ForeignKey(Student, on_delete=models.CASCADE)
    courseid = models.ForeignKey(Course, on_delete=models.CASCADE)


class StatusUpdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.TextField(validators=[MaxLengthValidator(200)])
    datepost = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Status update by {self.user.username} at {self.created_at}"


class Fileupload(models.Model):
    filename = models.CharField(max_length=20)
    files = models.FileField(upload_to='documents/%Y/%m/%d/')
    timeuploaded = models.DateTimeField(auto_now_add=True)
    courseid = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Notification(models.Model):
    studentid = models.ForeignKey(User, on_delete=models.CASCADE)
    courseid = models.ForeignKey(Course, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class StudentNotification(models.Model):
    teacherid = models.ForeignKey(User, on_delete=models.CASCADE)
    courseid = models.ForeignKey(Course, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USERTYPES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    usertype = models.CharField(max_length=10, choices=USERTYPES)
    studentid = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    teacherid = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username




