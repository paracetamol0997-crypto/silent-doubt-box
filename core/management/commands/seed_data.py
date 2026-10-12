from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import User, Subject, Doubt


class Command(BaseCommand):
    help = "Seeds database with demo students, teachers, subjects, and doubts"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding demo data for Silent Classroom Doubt Box..."))

        # 1. Subjects
        subjects_data = [
            ("Data Structures", "CS201", "Core algorithmic data structures like arrays, trees, graphs, stacks, queues."),
            ("Database Management Systems", "CS301", "Relational database concepts, SQL, normalization, transactions, and indexing."),
            ("Computer Networks", "CS302", "OSI model, TCP/IP protocol suite, routing algorithms, and network security."),
            ("Operating Systems", "CS202", "Processes, threads, CPU scheduling, synchronization, deadlocks, and memory management."),
            ("Machine Learning", "CS401", "Supervised and unsupervised learning, neural networks, loss functions, and evaluation metrics."),
            ("Python Programming", "CS102", "Python syntax, OOP, modules, data manipulation, and scripting."),
            ("Java Programming", "CS103", "Object-oriented principles, JVM internals, multithreading, and collections framework."),
            ("Computer Organization & Architecture", "CS203", "Instruction sets, ALU, memory hierarchy, pipelining, and cache memory."),
            ("Software Engineering", "CS303", "SDLC models, agile methodology, software testing, architecture, and design patterns."),
        ]

        created_subjects = {}
        for name, code, desc in subjects_data:
            subject, _ = Subject.objects.get_or_create(
                name=name,
                defaults={'code': code, 'description': desc}
            )
            created_subjects[name] = subject
        self.stdout.write(self.style.SUCCESS(f"[OK] Created/verified {len(created_subjects)} subjects."))

        # 2. Teachers
        teachers_data = [
            ("T101", "Dr. Ramesh Sharma", "teacher@123", "ramesh@college.edu"),
            ("T102", "Prof. Anjali Verma", "teacher@123", "anjali@college.edu"),
        ]

        created_teachers = {}
        for tid, name, pwd, email in teachers_data:
            user, created = User.objects.get_or_create(
                teacher_id=tid,
                defaults={
                    'username': tid.lower(),
                    'name': name,
                    'role': 'TEACHER',
                    'email': email,
                    'is_staff': True,
                }
            )
            user.set_password(pwd)
            user.name = name
            user.role = 'TEACHER'
            user.save()
            created_teachers[tid] = user
        self.stdout.write(self.style.SUCCESS(f"[OK] Created/verified {len(created_teachers)} teachers."))

        # 3. Students
        students_data = [
            ("23CSE101", "Rahul Kumar", "rahul@123", "rahul@student.college.edu"),
            ("23CSE102", "Priya Sharma", "priya@123", "priya@student.college.edu"),
            ("23CSE103", "Arjun Patel", "arjun@123", "arjun@student.college.edu"),
            ("23CSE104", "Sneha Reddy", "sneha@123", "sneha@student.college.edu"),
        ]

        created_students = {}
        for reg_no, name, pwd, email in students_data:
            user, created = User.objects.get_or_create(
                register_number=reg_no,
                defaults={
                    'username': reg_no.lower(),
                    'name': name,
                    'role': 'STUDENT',
                    'email': email,
                }
            )
            user.set_password(pwd)
            user.name = name
            user.role = 'STUDENT'
            user.save()
            created_students[reg_no] = user
        self.stdout.write(self.style.SUCCESS(f"[OK] Created/verified {len(created_students)} students."))

        # 4. Sample Doubts
        # Clear previous sample doubts to maintain clean state
        Doubt.objects.all().delete()

        now = timezone.now()

        # Rahul's Doubts
        Doubt.objects.create(
            student=created_students["23CSE101"],
            subject=created_subjects["Data Structures"],
            question="I don't understand how recursion works. Why does the function not get stuck in an infinite loop without a base condition?",
            status="PENDING",
            created_at=now - timedelta(hours=3),
        )

        Doubt.objects.create(
            student=created_students["23CSE101"],
            subject=created_subjects["Database Management Systems"],
            question="What is the primary difference between Clustered and Non-Clustered indexes in SQL databases?",
            status="CLARIFIED",
            teacher_answer="A clustered index defines how the actual table rows are physically stored on disk (sorted by key). Therefore, a table can only have ONE clustered index. A non-clustered index is a separate index structure stored apart from the table, containing pointers to the actual data rows. Think of it like the index at the back of a textbook.",
            answered_by=created_teachers["T101"],
            created_at=now - timedelta(days=1, hours=5),
            answered_at=now - timedelta(days=1, hours=2),
        )

        # Priya's Doubts
        Doubt.objects.create(
            student=created_students["23CSE102"],
            subject=created_subjects["Computer Networks"],
            question="How does the three-way handshake work in TCP before reliable transmission begins? What happens if the ACK gets lost?",
            status="PENDING",
            created_at=now - timedelta(hours=6),
        )

        Doubt.objects.create(
            student=created_students["23CSE102"],
            subject=created_subjects["Python Programming"],
            question="Why is Python classified as an interpreted language when .pyc bytecode files are visibly generated in __pycache__?",
            status="CLARIFIED",
            teacher_answer="Great question, Priya! Python compiles source code (.py) into intermediate bytecode (.pyc) first, but that bytecode is not executed directly by CPU hardware. Instead, the Python Virtual Machine (PVM) interprets each bytecode instruction on the fly. Because bytecode execution happens through a runtime interpreter rather than compiling ahead-of-time to native machine binary, Python is called interpreted.",
            answered_by=created_teachers["T102"],
            created_at=now - timedelta(days=2),
            answered_at=now - timedelta(days=1, hours=8),
        )

        # Arjun's Doubts
        Doubt.objects.create(
            student=created_students["23CSE103"],
            subject=created_subjects["Operating Systems"],
            question="Can you explain how the Round Robin scheduling algorithm prevents starvation for CPU-bound processes?",
            status="PENDING",
            created_at=now - timedelta(hours=1),
        )

        # Sneha's Doubts
        Doubt.objects.create(
            student=created_students["23CSE104"],
            subject=created_subjects["Machine Learning"],
            question="What is the bias-variance tradeoff and how does L2 regularization (Ridge) help prevent overfitting in high-dimensional datasets?",
            status="PENDING",
            created_at=now - timedelta(minutes=45),
        )

        self.stdout.write(self.style.SUCCESS("[OK] Seeded realistic doubts (Pending and Clarified)."))
        self.stdout.write(self.style.SUCCESS("Demo database setup complete!"))
