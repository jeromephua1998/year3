from django.shortcuts import render
from .models import *
from .forms import UserForm, UserProfileForm, CourseForm, CourseEnrollmentForm,FeedbackForm, StatusUpdateForm, FileUpload, User, SearchForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm, UserProfileForm
from .models import AppUser, Student, Teacher

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('../login')


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user  

            usertype = profile_form.cleaned_data['usertype']

            if usertype == 'student':
                student = Student.objects.create(
                    studentemail=user.email,
                    studentFirstName=user.first_name,
                    studentLastName=user.last_name
                )
                profile.studentid = student
                profile.save()
                registered = True
            elif usertype == 'teacher':
                teacher = Teacher.objects.create(
                    teacheremail=user.email,
                    teacherFirstName=user.first_name,
                    teacherLastName=user.last_name
                )
                profile.teacherid = teacher
                profile.save()
                registered = True

            return redirect('login')

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'registration.html', {'user_form': user_form, 'profile_form': profile_form})


def user_login(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']


        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                pass
        else:
             return render(request, 'login.html', {'error_message': 'Invalid details.'})
    else:
        return render(request, 'login.html')


def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            user_profile = AppUser.objects.get(user=request.user)
            if user_profile and user_profile.teacherid:
                teacher_ids = user_profile.teacherid.pk
                course = form.save(commit=False)
                course.teacherid_id = teacher_ids
                course.save()

                # print(f"Course saved successfully for teacher ID: {teacher_id}")
            else:
                print("User profile or teacher ID not found.")
        else:
            print("Invalid form")
    else:
        form = CourseForm()
    return render(request, 'createcourse.html', {'form': form})



def home_view(request):
    user_profile = AppUser.objects.get(user=request.user)
    teacher_id = None
    student_id = None
    courses = None
    enrollments = None
    notifications = None
    studnotifications = None

    if user_profile.usertype == 'student':
        if user_profile.studentid:
            student_id = user_profile.studentid.pk
            enrollments = CourseEnrollment.objects.filter(studentid=user_profile.studentid)

            studnotifications = StudentNotification.objects.order_by('-timestamp')[:10]

    elif user_profile.usertype == 'teacher':
        if user_profile.teacherid:
            teacher_id = user_profile.teacherid.pk
            courses = Course.objects.filter(teacherid=user_profile.teacherid)

            notifications = Notification.objects.order_by('-timestamp')[:10]

    statusupdates= StatusUpdate.objects.all()


    return render(request, 'home.html', {'user_profile': user_profile, 'teacher_id': teacher_id, 'student_id': student_id,'courses': courses, 'enrollments': enrollments, 'statusupdates': statusupdates, 'notifications': notifications, 'studnotifications': studnotifications})



def enroll_course(request):
    courses = Course.objects.all()
    user_profile = AppUser.objects.get(user=request.user)
    print("User Profile:", user_profile)

    if request.method == 'POST':
        form = CourseEnrollmentForm(request.POST)
        print("Form Data:", request.POST)
        
        if form.is_valid():
            enrol = form.save(commit=False) 
            if user_profile.studentid:
                student_id = user_profile.studentid.pk
                enrol.studentid_id = student_id
                enrol.save()

                course_id = form.cleaned_data['courseid']
                notification = Notification.objects.create(
                    studentid=request.user, 
                    courseid=course_id,
                    timestamp=timezone.now()
                )
            else:
                pass
        else:
            print("Form is invalid.")
    else:
        form = CourseEnrollment()
    return render(request, 'enrollcourse.html', {'form': form, 'courses': courses})



def submit_feedback(request):
    user_profile = AppUser.objects.get(user=request.user)
    courses = Course.objects.all()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.studentid = user_profile.studentid 
            course_id = request.POST.get('courseid')    
            course = Course.objects.get(pk=course_id)
            feedback.courseid = course  
            feedback.save()
            return redirect('home')  
    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {'form': form, 'courses': courses})

def view_students(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollments = CourseEnrollment.objects.filter(courseid=course)

    students = []
    for enrollment in enrollments:
        student = Student.objects.get(pk=enrollment.studentid_id)
        students.append(student)

    return render(request, 'viewstudent.html', {'course': course, 'students': students})


def status_update(request):
    if request.method == 'POST':
        form = StatusUpdateForm(request.POST)
        if form.is_valid():
            status_update = form.save(commit=False)
            status_update.user = request.user
            status_update.save()
            return redirect('home')  # Redirect to the home page after submission
    else:
        form = StatusUpdateForm()
    return render(request, 'statusupdate.html', {'form': form})


def manage_students(request):
    students = Student.objects.all()
    return render(request, 'managestudents.html', {'students': students})

def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    student.delete()
    return redirect('manage_students')


def upload_file(request):
    courses = Course.objects.all()
    if request.method == 'POST':
        form = FileUpload(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['files'] 
            filename = form.cleaned_data['filename']
            course_id = request.POST.get('courseid')

            course = Course.objects.get(pk=course_id)
            upload = Fileupload(files=file, filename=filename, courseid=course)  
            upload.save()  
        
            course_id = form.cleaned_data['courseid']
            notification = StudentNotification.objects.create(
                teacherid=request.user, 
                courseid=course_id,
                timestamp=timezone.now()
                )
        else:
            pass
    else:
        form = FileUpload()
    return render(request, 'upload.html', {'form': form, 'courses': courses})


def course_material(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course_materials = Fileupload.objects.filter(courseid=course)
    return render(request, 'coursematerial.html', {'course': course, 'course_materials': course_materials})

def view_feedback(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    feedbacks = CourseFeedback.objects.filter(courseid=course)
    return render(request, 'viewfeedback.html', {'feedbacks': feedbacks})
    

def search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']
            teachers = Teacher.objects.filter(teacherFirstName__icontains=query) 
            students = Student.objects.filter(studentFirstName__icontains=query) 
            return render(request, 'search.html', {'teachers': teachers, 'students': students, 'query': query})
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form})