from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """
    Unified User model supporting both Student and Teacher roles
    with strict role separation and dedicated identifiers.
    """
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('TEACHER', 'Teacher'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    name = models.CharField(max_length=150, help_text="Full Name of Student or Teacher")

    # Student specific field
    register_number = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        help_text="College Register Number (e.g., 23CSE101)"
    )

    # Teacher specific field
    teacher_id = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        help_text="Faculty / Teacher ID (e.g., T101)"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_student(self):
        return self.role == 'STUDENT'

    @property
    def is_teacher(self):
        return self.role == 'TEACHER'

    def display_identifier(self):
        if self.is_student:
            return self.register_number or self.username
        elif self.is_teacher:
            return self.teacher_id or self.username
        return self.username

    def __str__(self):
        if self.is_student:
            return f"{self.register_number} - {self.name}"
        elif self.is_teacher:
            return f"{self.teacher_id} - {self.name}"
        return self.username


class Subject(models.Model):
    """
    Academic subjects available for students to select when posting doubts.
    Managed dynamically in the database.
    """
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.name


class Doubt(models.Model):
    """
    Private doubt submitted by a student.
    Strict privacy rule:
    - Only the student who submitted it can view it.
    - Teachers can view doubts from all students and provide answers.
    - Other students can never access or view this doubt.
    """
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CLARIFIED', 'Clarified'),
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submitted_doubts',
        limit_choices_to={'role': 'STUDENT'}
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='doubts'
    )
    question = models.TextField(help_text="Student's private doubt/question")
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    teacher_answer = models.TextField(blank=True, null=True, help_text="Answer submitted by the teacher")
    answered_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clarified_doubts',
        limit_choices_to={'role': 'TEACHER'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Doubt'
        verbose_name_plural = 'Doubts'

    def mark_clarified(self, teacher, answer_text):
        """Helper method to answer and mark the doubt clarified."""
        self.teacher_answer = answer_text
        self.answered_by = teacher
        self.status = 'CLARIFIED'
        self.answered_at = timezone.now()
        self.save()

    def __str__(self):
        return f"[{self.subject.name}] {self.student.name} ({self.status})"
