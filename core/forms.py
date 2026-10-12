from django import forms
from .models import User, Subject, Doubt


class StudentLoginForm(forms.Form):
    register_number = forms.CharField(
        max_length=50,
        required=True,
        error_messages={'required': 'Please enter your register number.'},
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'e.g. 23CSE101',
            'autocomplete': 'off',
            'autofocus': True,
        })
    )
    student_name = forms.CharField(
        max_length=150,
        required=True,
        error_messages={'required': 'Please enter your name.'},
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'e.g. Rahul Kumar',
            'autocomplete': 'name',
        })
    )
    password = forms.CharField(
        required=True,
        error_messages={'required': 'Please enter your password.'},
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '••••••••',
            'autocomplete': 'current-password',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        register_number = cleaned_data.get('register_number', '').strip()
        student_name = cleaned_data.get('student_name', '').strip()
        password = cleaned_data.get('password')

        if register_number and student_name and password:
            try:
                user = User.objects.get(register_number__iexact=register_number, role='STUDENT')
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid login details. Student register number not found.")

            if not user.check_password(password):
                raise forms.ValidationError("Invalid login details. Incorrect password.")

            # Validate student name matches
            if user.name.strip().lower() != student_name.lower():
                raise forms.ValidationError("Student name does not match the register number record.")

            if not user.is_active:
                raise forms.ValidationError("This student account has been deactivated.")

            cleaned_data['user'] = user

        return cleaned_data


class TeacherLoginForm(forms.Form):
    teacher_id = forms.CharField(
        max_length=50,
        required=True,
        error_messages={'required': 'Please enter your teacher ID.'},
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'e.g. T101',
            'autocomplete': 'off',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        required=True,
        error_messages={'required': 'Please enter your password.'},
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '••••••••',
            'autocomplete': 'current-password',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        teacher_id = cleaned_data.get('teacher_id', '').strip()
        password = cleaned_data.get('password')

        if teacher_id and password:
            try:
                user = User.objects.get(teacher_id__iexact=teacher_id, role='TEACHER')
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid login details. Teacher ID not found.")

            if not user.check_password(password):
                raise forms.ValidationError("Invalid login details. Incorrect password.")

            if not user.is_active:
                raise forms.ValidationError("This teacher account has been deactivated.")

            cleaned_data['user'] = user

        return cleaned_data


class DoubtForm(forms.ModelForm):
    class Meta:
        model = Doubt
        fields = ['subject', 'question']
        error_messages = {
            'subject': {
                'required': 'Please select a subject.'
            },
            'question': {
                'required': 'Please enter your doubt.'
            }
        }
        widgets = {
            'subject': forms.Select(attrs={
                'class': 'form-select',
                'id': 'doubt-subject-select',
            }),
            'question': forms.Textarea(attrs={
                'class': 'form-textarea',
                'id': 'doubt-question-input',
                'rows': 5,
                'placeholder': 'What would you like to ask? (e.g. Sir, I am not understanding the difference between stack and queue. Can you please explain it?)',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].empty_label = "-- Select Subject --"
        self.fields['subject'].queryset = Subject.objects.all().order_by('name')

    def clean_question(self):
        question = self.cleaned_data.get('question', '').strip()
        if not question:
            raise forms.ValidationError("Please enter your doubt.")
        if len(question) < 5:
            raise forms.ValidationError("Your doubt is too short. Please describe what you need help with.")
        return question


class TeacherAnswerForm(forms.Form):
    teacher_answer = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'id': 'teacher-answer-input',
            'rows': 6,
            'placeholder': 'Write your answer here...',
        }),
        required=True,
        error_messages={'required': 'Please write your answer before submitting.'}
    )

    def clean_teacher_answer(self):
        answer = self.cleaned_data.get('teacher_answer', '').strip()
        if not answer:
            raise forms.ValidationError("Please write your answer before submitting.")
        return answer
