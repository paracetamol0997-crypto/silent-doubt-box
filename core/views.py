from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.utils import timezone

from .models import User, Subject, Doubt
from .forms import StudentLoginForm, TeacherLoginForm, DoubtForm, TeacherAnswerForm
from .decorators import student_required, teacher_required


def landing_view(request):
    """
    Public landing page for 'Silent Classroom Doubt Box'.
    Directs students and teachers to their respective login portals.
    """
    if request.user.is_authenticated:
        if request.user.is_student:
            return redirect('student_dashboard')
        elif request.user.is_teacher:
            return redirect('teacher_dashboard')

    subjects = Subject.objects.all().order_by('name')[:6]
    total_students = User.objects.filter(role='STUDENT').count()
    total_doubts = Doubt.objects.count()
    clarified_doubts = Doubt.objects.filter(status='CLARIFIED').count()

    context = {
        'subjects': subjects,
        'total_students': total_students,
        'total_doubts': total_doubts,
        'clarified_doubts': clarified_doubts,
    }
    return render(request, 'landing.html', context)


def student_login_view(request):
    """
    Authentication portal for students using:
    - College Register Number
    - Student Name
    - Password
    """
    if request.user.is_authenticated:
        if request.user.is_student:
            return redirect('student_dashboard')
        return redirect('teacher_dashboard')

    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            messages.success(request, f"Welcome back, {user.name}!")
            next_url = request.GET.get('next')
            if next_url and next_url.startswith('/student/'):
                return redirect(next_url)
            return redirect('student_dashboard')
        else:
            # Let form errors render in template
            pass
    else:
        form = StudentLoginForm()

    return render(request, 'auth/student_login.html', {'form': form})


def teacher_login_view(request):
    """
    Authentication portal for teachers using:
    - Teacher ID
    - Password
    """
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teacher_dashboard')
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            messages.success(request, f"Welcome, Prof. {user.name}!")
            next_url = request.GET.get('next')
            if next_url and next_url.startswith('/teacher/'):
                return redirect(next_url)
            return redirect('teacher_dashboard')
        else:
            pass
    else:
        form = TeacherLoginForm()

    return render(request, 'auth/teacher_login.html', {'form': form})


def logout_view(request):
    """
    Logs out the user and redirects to the landing page.
    """
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('landing')


# ==========================================
# STUDENT PORTAL VIEWS (Strict Privacy)
# ==========================================

@student_required
def student_dashboard_view(request):
    """
    Clean, distraction-free student dashboard.
    Displays student info, summary statistics, and quick navigation.
    """
    student = request.user
    student_doubts = Doubt.objects.filter(student=student)

    total_doubts = student_doubts.count()
    pending_doubts = student_doubts.filter(status='PENDING').count()
    clarified_doubts = student_doubts.filter(status='CLARIFIED').count()

    recent_doubts = student_doubts.select_related('subject')[:5]

    context = {
        'student': student,
        'total_doubts': total_doubts,
        'pending_doubts': pending_doubts,
        'clarified_doubts': clarified_doubts,
        'recent_doubts': recent_doubts,
    }
    return render(request, 'student/dashboard.html', context)


@student_required
def ask_doubt_view(request):
    """
    Private doubt submission view for students.
    Only allows selecting a subject and typing the question.
    """
    if request.method == 'POST':
        form = DoubtForm(request.POST)
        if form.is_valid():
            doubt = form.save(commit=False)
            doubt.student = request.user  # strictly bound to the authenticated student
            doubt.status = 'PENDING'
            doubt.save()
            messages.success(request, "Your doubt has been submitted privately. Your teacher will review it soon.")
            return redirect('student_my_doubts')
    else:
        form = DoubtForm()

    context = {
        'form': form,
        'student': request.user,
    }
    return render(request, 'student/ask_doubt.html', context)


@student_required
def student_my_doubts_view(request):
    """
    Shows ONLY doubts submitted by the currently logged-in student.
    Strict privacy: Student A will never see Student B's doubts.
    """
    student = request.user
    doubts = Doubt.objects.filter(student=student).select_related('subject', 'answered_by')

    # Subject filter
    subject_id = request.GET.get('subject')
    if subject_id:
        doubts = doubts.filter(subject_id=subject_id)

    # Status filter
    status = request.GET.get('status')
    if status in ['PENDING', 'CLARIFIED']:
        doubts = doubts.filter(status=status)

    subjects = Subject.objects.all().order_by('name')

    context = {
        'doubts': doubts,
        'subjects': subjects,
        'selected_subject': subject_id,
        'selected_status': status,
        'student': student,
    }
    return render(request, 'student/my_doubts.html', context)


@student_required
def student_doubt_detail_view(request, doubt_id):
    """
    Detailed view of a single doubt submitted by the logged-in student.
    CRITICAL SECURITY CHECK:
    If the doubt does not belong to the current student, reject with 403 Forbidden.
    """
    doubt = get_object_or_404(Doubt, id=doubt_id)

    # Strict ownership verification
    if doubt.student != request.user:
        raise PermissionDenied("Privacy Violation: You are not authorized to view another student's doubt.")

    context = {
        'doubt': doubt,
        'student': request.user,
    }
    return render(request, 'student/doubt_detail.html', context)


# ==========================================
# TEACHER PORTAL VIEWS (Full Oversight)
# ==========================================

@teacher_required
def teacher_dashboard_view(request):
    """
    Teacher overview dashboard showing:
    - Total Students
    - Total Doubts
    - Pending Doubts
    - Clarified Doubts
    """
    total_students = User.objects.filter(role='STUDENT').count()
    total_doubts = Doubt.objects.count()
    pending_doubts = Doubt.objects.filter(status='PENDING').count()
    clarified_doubts = Doubt.objects.filter(status='CLARIFIED').count()

    recent_pending = Doubt.objects.filter(status='PENDING').select_related('student', 'subject')[:6]
    recent_clarified = Doubt.objects.filter(status='CLARIFIED').select_related('student', 'subject', 'answered_by')[:4]

    # Subject breakdown
    subject_stats = Subject.objects.annotate(
        total_doubts=Count('doubts'),
        pending_doubts=Count('doubts', filter=Q(doubts__status='PENDING')),
        clarified_doubts=Count('doubts', filter=Q(doubts__status='CLARIFIED')),
    ).order_by('-total_doubts')[:5]

    context = {
        'teacher': request.user,
        'total_students': total_students,
        'total_doubts': total_doubts,
        'pending_doubts': pending_doubts,
        'clarified_doubts': clarified_doubts,
        'recent_pending': recent_pending,
        'recent_clarified': recent_clarified,
        'subject_stats': subject_stats,
    }
    return render(request, 'teacher/dashboard.html', context)


@teacher_required
def teacher_all_doubts_view(request):
    """
    All Student Doubts page.
    Displays doubts from all students with combined filtering:
    - Filter by Subject
    - Filter by Status (Pending / Clarified)
    - Search by student name or register number
    """
    doubts = Doubt.objects.all().select_related('student', 'subject', 'answered_by')

    # Subject filter
    subject_id = request.GET.get('subject')
    if subject_id:
        doubts = doubts.filter(subject_id=subject_id)

    # Status filter
    status = request.GET.get('status')
    if status in ['PENDING', 'CLARIFIED']:
        doubts = doubts.filter(status=status)

    # Search filter
    search_query = request.GET.get('search', '').strip()
    if search_query:
        doubts = doubts.filter(
            Q(student__name__icontains=search_query) |
            Q(student__register_number__icontains=search_query) |
            Q(question__icontains=search_query)
        )

    subjects = Subject.objects.all().order_by('name')

    context = {
        'doubts': doubts,
        'subjects': subjects,
        'selected_subject': subject_id,
        'selected_status': status,
        'search_query': search_query,
        'teacher': request.user,
    }
    return render(request, 'teacher/all_doubts.html', context)


@teacher_required
def teacher_answer_doubt_view(request, doubt_id):
    """
    Teacher opens a doubt to review and write an answer.
    After submission:
    - Save teacher answer
    - Status changes from Pending to Clarified
    - Visible to that specific student in 'My Doubts'
    """
    doubt = get_object_or_404(Doubt.objects.select_related('student', 'subject', 'answered_by'), id=doubt_id)

    if request.method == 'POST':
        form = TeacherAnswerForm(request.POST)
        if form.is_valid():
            answer_text = form.cleaned_data['teacher_answer']
            doubt.mark_clarified(request.user, answer_text)
            messages.success(
                request,
                f"Answer recorded successfully for {doubt.student.name} ({doubt.student.register_number}). Status updated to Clarified."
            )
            return redirect('teacher_all_doubts')
    else:
        # Pre-fill existing answer if already answered
        initial_data = {}
        if doubt.teacher_answer:
            initial_data['teacher_answer'] = doubt.teacher_answer
        form = TeacherAnswerForm(initial=initial_data)

    context = {
        'doubt': doubt,
        'form': form,
        'teacher': request.user,
    }
    return render(request, 'teacher/answer_doubt.html', context)


@teacher_required
def teacher_students_list_view(request):
    """
    List of registered students with statistics on doubts submitted.
    """
    search_query = request.GET.get('search', '').strip()
    students = User.objects.filter(role='STUDENT').annotate(
        doubts_count=Count('submitted_doubts'),
        pending_count=Count('submitted_doubts', filter=Q(submitted_doubts__status='PENDING')),
        clarified_count=Count('submitted_doubts', filter=Q(submitted_doubts__status='CLARIFIED')),
    ).order_by('register_number')

    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) |
            Q(register_number__icontains=search_query)
        )

    context = {
        'students': students,
        'search_query': search_query,
        'teacher': request.user,
    }
    return render(request, 'teacher/students_list.html', context)


# ==========================================
# CUSTOM ERROR HANDLERS
# ==========================================

def permission_denied_view(request, exception=None):
    """Custom 403 Forbidden handler highlighting privacy isolation."""
    return render(request, 'errors/403.html', {'exception': exception}, status=403)


def page_not_found_view(request, exception=None):
    """Custom 404 Not Found handler."""
    return render(request, 'errors/404.html', {'exception': exception}, status=404)
