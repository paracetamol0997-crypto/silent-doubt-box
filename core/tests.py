from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from core.models import User, Subject, Doubt


class SilentDoubtBoxTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create Subjects
        self.subj_ds = Subject.objects.create(name="Data Structures", code="CS201")
        self.subj_dbms = Subject.objects.create(name="Database Management Systems", code="CS301")
        self.subj_os = Subject.objects.create(name="Operating Systems", code="CS202")

        # Create Students
        self.student_rahul = User.objects.create_user(
            username="23cse101",
            register_number="23CSE101",
            name="Rahul Kumar",
            role="STUDENT",
            password="rahul@123"
        )
        self.student_priya = User.objects.create_user(
            username="23cse102",
            register_number="23CSE102",
            name="Priya Sharma",
            role="STUDENT",
            password="priya@123"
        )

        # Create Teacher
        self.teacher_ramesh = User.objects.create_user(
            username="t101",
            teacher_id="T101",
            name="Dr. Ramesh Sharma",
            role="TEACHER",
            password="teacher@123"
        )

        # Create an initial doubt for Rahul
        self.rahul_doubt = Doubt.objects.create(
            student=self.student_rahul,
            subject=self.subj_ds,
            question="Why does recursion need a base condition?",
            status="PENDING"
        )

        # Create an initial doubt for Priya
        self.priya_doubt = Doubt.objects.create(
            student=self.student_priya,
            subject=self.subj_os,
            question="How does Round Robin scheduling work?",
            status="PENDING"
        )

    # 1. Student can log in
    def test_student_login_success(self):
        response = self.client.post(reverse('student_login'), {
            'register_number': '23CSE101',
            'student_name': 'Rahul Kumar',
            'password': 'rahul@123',
        })
        self.assertRedirects(response, reverse('student_dashboard'))
        self.assertEqual(int(self.client.session['_auth_user_id']), self.student_rahul.id)

    # Validation: Student login fails with wrong password
    def test_student_login_invalid_password(self):
        response = self.client.post(reverse('student_login'), {
            'register_number': '23CSE101',
            'student_name': 'Rahul Kumar',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid login details")

    # Validation: Student login fails with mismatched name
    def test_student_login_mismatched_name(self):
        response = self.client.post(reverse('student_login'), {
            'register_number': '23CSE101',
            'student_name': 'Wrong Name',
            'password': 'rahul@123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student name does not match")

    # 2. Teacher can log in
    def test_teacher_login_success(self):
        response = self.client.post(reverse('teacher_login'), {
            'teacher_id': 'T101',
            'password': 'teacher@123',
        })
        self.assertRedirects(response, reverse('teacher_dashboard'))
        self.assertEqual(int(self.client.session['_auth_user_id']), self.teacher_ramesh.id)

    # 3. Student can submit a doubt
    def test_student_submit_doubt(self):
        self.client.force_login(self.student_rahul)
        response = self.client.post(reverse('ask_doubt'), {
            'subject': self.subj_dbms.id,
            'question': 'What is the difference between primary key and foreign key in SQL?',
        })
        self.assertRedirects(response, reverse('student_my_doubts'))
        
        # Verify doubt exists in database and is attached to Rahul
        new_doubt = Doubt.objects.filter(student=self.student_rahul, subject=self.subj_dbms).first()
        self.assertIsNotNone(new_doubt)
        self.assertEqual(new_doubt.status, 'PENDING')
        self.assertIn("difference between primary key", new_doubt.question)

    # Validation: Student cannot submit empty doubt
    def test_student_submit_empty_doubt_rejected(self):
        self.client.force_login(self.student_rahul)
        response = self.client.post(reverse('ask_doubt'), {
            'subject': self.subj_dbms.id,
            'question': '   ',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter your doubt")

    # 4. Teacher can see the doubt
    def test_teacher_can_see_all_doubts(self):
        self.client.force_login(self.teacher_ramesh)
        response = self.client.get(reverse('teacher_all_doubts'))
        self.assertEqual(response.status_code, 200)
        # Teacher must see both Rahul's and Priya's doubts
        self.assertContains(response, "Why does recursion need a base condition?")
        self.assertContains(response, "How does Round Robin scheduling work?")
        self.assertContains(response, "Rahul Kumar")
        self.assertContains(response, "Priya Sharma")

    # 5. Teacher can answer the doubt
    def test_teacher_can_answer_doubt(self):
        self.client.force_login(self.teacher_ramesh)
        answer_text = "Recursion requires a base condition to terminate the stack frames, otherwise stack overflow occurs."
        response = self.client.post(reverse('teacher_answer_doubt', args=[self.rahul_doubt.id]), {
            'teacher_answer': answer_text,
        })
        self.assertRedirects(response, reverse('teacher_all_doubts'))

        # Verify doubt status updated in DB
        self.rahul_doubt.refresh_from_db()
        self.assertEqual(self.rahul_doubt.status, 'CLARIFIED')
        self.assertEqual(self.rahul_doubt.teacher_answer, answer_text)
        self.assertEqual(self.rahul_doubt.answered_by, self.teacher_ramesh)
        self.assertIsNotNone(self.rahul_doubt.answered_at)

    # 6. Student can see the answer
    def test_student_sees_teacher_answer(self):
        # Teacher answers first
        self.rahul_doubt.mark_clarified(
            self.teacher_ramesh,
            "The base condition prevents endless recursive calls."
        )

        # Rahul logs in and checks My Doubts
        self.client.force_login(self.student_rahul)
        response = self.client.get(reverse('student_my_doubts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The base condition prevents endless recursive calls.")
        self.assertContains(response, "Dr. Ramesh Sharma")
        self.assertContains(response, "Clarified")

    # 7. Student A cannot see Student B's doubts (Strict Isolation)
    def test_student_a_cannot_see_student_b_doubts(self):
        self.client.force_login(self.student_priya)
        response = self.client.get(reverse('student_my_doubts'))
        self.assertEqual(response.status_code, 200)
        
        # Priya should see her own doubt
        self.assertContains(response, "How does Round Robin scheduling work?")
        # Priya must NEVER see Rahul's doubt
        self.assertNotContains(response, "Why does recursion need a base condition?")
        self.assertNotContains(response, "Rahul Kumar")
        self.assertNotContains(response, "23CSE101")

    # 8. Student cannot access teacher dashboard (Role Authorization)
    def test_student_cannot_access_teacher_dashboard(self):
        self.client.force_login(self.student_rahul)
        # Should raise PermissionDenied (403)
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 403)

    # 9. Student cannot access or modify another student's doubt through URL manipulation
    def test_student_cannot_access_other_student_doubt_detail(self):
        self.client.force_login(self.student_rahul)
        # Rahul tries to access Priya's doubt ID
        response = self.client.get(reverse('student_doubt_detail', args=[self.priya_doubt.id]))
        # Must return 403 Forbidden
        self.assertEqual(response.status_code, 403)

    # 10. Teacher can filter by subject
    def test_teacher_filter_by_subject(self):
        self.client.force_login(self.teacher_ramesh)
        # Filter for Data Structures
        response = self.client.get(f"{reverse('teacher_all_doubts')}?subject={self.subj_ds.id}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Why does recursion need a base condition?")
        self.assertNotContains(response, "How does Round Robin scheduling work?")

    # 11. Teacher can filter by status
    def test_teacher_filter_by_status(self):
        # Clarify Rahul's doubt
        self.rahul_doubt.mark_clarified(self.teacher_ramesh, "Explained recursion")
        self.client.force_login(self.teacher_ramesh)

        # Filter for PENDING doubts only
        response_pending = self.client.get(f"{reverse('teacher_all_doubts')}?status=PENDING")
        self.assertEqual(response_pending.status_code, 200)
        self.assertContains(response_pending, "How does Round Robin scheduling work?")
        self.assertNotContains(response_pending, "Why does recursion need a base condition?")

        # Filter for CLARIFIED doubts only
        response_clarified = self.client.get(f"{reverse('teacher_all_doubts')}?status=CLARIFIED")
        self.assertEqual(response_clarified.status_code, 200)
        self.assertContains(response_clarified, "Why does recursion need a base condition?")
        self.assertNotContains(response_clarified, "How does Round Robin scheduling work?")

    # 12. Teacher can search students by name or register number
    def test_teacher_search_students(self):
        self.client.force_login(self.teacher_ramesh)

        # Search by student name
        response_name = self.client.get(f"{reverse('teacher_all_doubts')}?search=Priya")
        self.assertEqual(response_name.status_code, 200)
        self.assertContains(response_name, "How does Round Robin scheduling work?")
        self.assertNotContains(response_name, "Why does recursion need a base condition?")

        # Search by register number
        response_reg = self.client.get(f"{reverse('teacher_all_doubts')}?search=23CSE101")
        self.assertEqual(response_reg.status_code, 200)
        self.assertContains(response_reg, "Why does recursion need a base condition?")
        self.assertNotContains(response_reg, "How does Round Robin scheduling work?")

    # 13. Logout works correctly
    def test_logout_redirects_and_clears_session(self):
        self.client.force_login(self.student_rahul)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('landing'))
        self.assertNotIn('_auth_user_id', self.client.session)

    # 14. Refreshing the page maintains the correct authenticated state
    def test_authenticated_state_persistence(self):
        self.client.force_login(self.student_rahul)
        # First visit
        res1 = self.client.get(reverse('student_dashboard'))
        self.assertEqual(res1.status_code, 200)
        self.assertContains(res1, "Rahul Kumar")
        # Second visit (page refresh)
        res2 = self.client.get(reverse('student_dashboard'))
        self.assertEqual(res2.status_code, 200)
        self.assertContains(res2, "Rahul Kumar")

    # 15. Mobile layout meta viewport present in base template
    def test_mobile_viewport_and_responsive_markup(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="viewport"')
        self.assertContains(response, 'width=device-width')
