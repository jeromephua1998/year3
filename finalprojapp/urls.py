from django.urls import include, path
from . import views
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('home/', views.home_view, name ='home'),
    path('createcourse/', views.create_course, name ='courses'),
    path('logout/', views.user_logout, name='logout'),
    path('enrollcourse/', views.enroll_course, name='enrollcourse'),
    path('feedback/', views.submit_feedback, name='feedback'),
    path('statusupdate/', views.status_update, name='statusupdate'),
    path('view_students/<int:course_id>/', views.view_students, name='view_students'),
    path('managestudents/', views.manage_students, name='manage_students'),
    path('deletestudents/<int:student_id>/', views.delete_student, name='delete_students'),
    path('upload/', views.upload_file, name = 'upload_file'),
    path('coursematerial/<int:course_id>/', views.course_material, name='course_material'),
    path('view_feedback/<int:course_id>/', views.view_feedback, name='view_feedback'),
    path('search/', views.search, name = 'search'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)