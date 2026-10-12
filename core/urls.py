from django.urls import path
from . import views

urlpatterns = [
    # Public & Auth
    path('', views.landing_view, name='landing'),
    path('login/student/', views.student_login_view, name='student_login'),
    path('login/teacher/', views.teacher_login_view, name='teacher_login'),
    path('logout/', views.logout_view, name='logout'),

    # Student Portal
    path('student/dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('student/ask/', views.ask_doubt_view, name='ask_doubt'),
    path('student/my-doubts/', views.student_my_doubts_view, name='student_my_doubts'),
    path('student/doubt/<int:doubt_id>/', views.student_doubt_detail_view, name='student_doubt_detail'),

    # Teacher Portal
    path('teacher/dashboard/', views.teacher_dashboard_view, name='teacher_dashboard'),
    path('teacher/doubts/', views.teacher_all_doubts_view, name='teacher_all_doubts'),
    path('teacher/doubt/<int:doubt_id>/answer/', views.teacher_answer_doubt_view, name='teacher_answer_doubt'),
    path('teacher/students/', views.teacher_students_list_view, name='teacher_students_list'),
]
