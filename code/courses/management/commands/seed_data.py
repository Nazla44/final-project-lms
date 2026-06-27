"""
Management command untuk mengisi database dengan data dummy.

Jalankan dengan:
    python manage.py seed_data

Data yang dibuat:
    - 1 Superuser Admin
    - 20 User pengajar (dosen01 - dosen20)
    - 80 User mahasiswa (mhs001 - mhs080)
    - 100 Course (mata kuliah)
    - 500 CourseMember (anggota kelas)
    - 300 CourseContent (konten/materi kelas)
    - 1000+ Comment (komentar pada konten)

Semua operasi INSERT menggunakan bulk_create (sesuai Modul 05 Bagian 6).
Command ini idempoten: aman dijalankan berulang kali tanpa membuat duplikat.

Referensi: Modul 05 - Bagian 6: Bulk Operations
"""

import random
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group  
from courses.models import Course, CourseMember, CourseContent, Comment
from django.utils import timezone
import pytz


FIRST_NAMES = [
    'Agus', 'Ani', 'Bambang', 'Cindy', 'Doni',
    'Eka', 'Fitri', 'Guntur', 'Hana', 'Irfan',
    'Joko', 'Kartika', 'Lukman', 'Mila', 'Nando',
    'Oktavia', 'Pratama', 'Qonita', 'Rama', 'Sinta',
]

LAST_NAMES = [
    'Abadi', 'Bhakti', 'Cahya', 'Darma', 'Erawan',
    'Firmansyah', 'Ginting', 'Hutagalung', 'Iskandar', 'Jaya',
    'Kurnia', 'Lubis', 'Mulyadi', 'Nugraha', 'Pangestu',
    'Ramadhan', 'Siregar', 'Tambunan', 'Utomo', 'Wibisono',
]

SUBJECTS = [
    'Pemrograman Dasar',
    'Database Lanjutan',
    'Struktur Data',
    'Jaringan Komputer Dasar',
    'Sistem Operasi Lanjutan',
    'Machine Learning',
    'Pengembangan Aplikasi Mobile',
    'Keamanan Jaringan',
    'Rekayasa Perangkat Lunak Lanjutan',
    'Python for Data Science',
    'Kotlin Programming',
    'Project Management IT',
    'System Analysis',
    'Cloud Computing',
    'Big Data Analytics',
    'Probabilitas dan Statistika',
    'Logika Matematika',
    'Computer Architecture',
    'Desain Grafis',
    'UX Design',
]

CONTENT_PREFIXES = [
    'Pendahuluan',
    'Dasar-Dasar',
    'Praktikum Mandiri',
    'Tugas Kelompok',
    'Evaluasi',
    'Modul Ajar',
    'Bahan Bacaan',
    'Studi Kasus',
    'Proyek Akhir',
    'Latihan Soal',
]

CONTENT_TOPICS = [
    'Variabel dan Fungsi',
    'Perulangan dan Kondisi',
    'Object Oriented Programming',
    'Database Design',
    'Query SQL dan Optimasi',
    'Normalisasi dan Denormalisasi',
    'RESTful API Design',
    'Autentikasi JWT',
    'Deployment dengan Docker',
    'Unit Testing & TDD',
    'Debugging Aplikasi',
    'Code Review Best Practice',
    'Git Flow',
    'Microservices Architecture',
    'Design Pattern',
    'Clean Architecture',
    'CI/CD Pipeline',
    'Monitoring dengan Grafana',
    'Logging & Observability',
    'API Documentation',
]

COMMENTS = [
    'Terima kasih, materi ini sangat membantu saya!',
    'Apakah ada contoh kasus nyata untuk topik ini?',
    'Saya masih kesulitan di bagian ini, bisa dibantu?',
    'Materinya keren dan aplikatif!',
    'Tugasnya menantang, tapi saya suka!',
    'Mohon bimbingan untuk tugas ini ya.',
    'Saya coba tapi error, tolong bantu cek.',
    'Jelasan dosen sangat mudah dipahami.',
    'Boleh pakai library lain untuk tugas ini?',
    'Saya setuju dengan pendapat teman di atas.',
    'Deadline tugas kapan ya?',
    'Boleh minta referensi tambahan?',
    'Bagian ini paling sulit menurut saya.',
    'Alhamdulillah, tugas selesai!',
    'Materi ini sangat relevan dengan industri.',
    'Ada video tambahan untuk materi ini?',
    'Terima kasih feedbacknya!',
    'Saya sudah coba ulang dan berhasil.',
    'Gaya mengajar dosennya asyik!',
    'Saya ingin mendalami topik ini lebih jauh.',
    'Terima kasih atas bimbingannya!',
    'Saya merekomendasikan materi ini.',
    'Bagus sekali, saya paham sekarang.',
    'Mohon diperjelas bagian ini.',
    'Saya akan coba terapkan di kerjaan.',
]

PRICES = [25000, 50000, 75000, 100000, 150000, 200000, 250000, 300000, 350000, 400000, 450000, 500000, 550000, 600000]


class Command(BaseCommand):
    help = 'Seed database dengan data dummy untuk Lab 05 Optimasi Database'

    def handle(self, *args, **options):
        random.seed(42)

        self.stdout.write(self.style.HTTP_INFO('=' * 60))
        self.stdout.write(self.style.HTTP_INFO('  SEEDING DATA - BERHASIL!!!'))
        self.stdout.write(self.style.HTTP_INFO('=' * 60))
        self.stdout.write('')

        self._seed_admin()
        teachers = self._seed_teachers()
        students = self._seed_students()
        courses = self._seed_courses(teachers)
        members = self._seed_members(courses, students)
        contents = self._seed_contents(courses)
        self._seed_comments(contents, members)

        self._print_summary()
        

        self.stdout.write(self.style.HTTP_INFO('AKUN DEMO:'))
        self.stdout.write('  [Admin]      admin / admin')
        self.stdout.write('  [Instructor] dosen / dosen')
        self.stdout.write('  [Student]    mahasiswa / mahasiswa')
        self.stdout.write('')
        
        self.stdout.write(self.style.HTTP_INFO('AKSES :'))
        self.stdout.write('  Swagger API    : http://localhost:8000/api/docs/')
        self.stdout.write('  Django Admin   : http://localhost:8000/admin/')
        self.stdout.write('  Silk Profiling : http://localhost:8000/silk/')
        self.stdout.write('  Flower Monitor : http://localhost:5555')
        self.stdout.write('  RabbitMQ       : http://localhost:15672 ')
        self.stdout.write('')
        
        self.stdout.write(self.style.HTTP_INFO(' Async Processing & Notification:'))
        self.stdout.write('  Enroll Async    : POST /api/enrollments-async')
        self.stdout.write('  Complete Course : POST /api/courses/{id}/complete-async')
        self.stdout.write('  Export Report   : POST /api/courses/{id}/export-async')
        self.stdout.write('  Update Stats    : POST /api/admin/update-stats')
        self.stdout.write('  Task Status     : GET  /api/tasks/{task_id}')
        self.stdout.write('')
        
      

    def _seed_admin(self):
        self.stdout.write('\n[0/6] Membuat SuperUser Admin...')
        
        wib = pytz.timezone('Asia/Jakarta')
        now_wib = timezone.now().astimezone(wib)
        
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@admin.com',
                'is_staff': True,
                'is_superuser': True,
                'date_joined': now_wib,
                'last_login': now_wib,
            }
        )
        if created:
            admin.set_password('admin')
            admin.save()
            self.stdout.write('  -> Admin Superuser ada')
        return admin

    def _seed_teachers(self):
        self.stdout.write('\n[1/6] Membuat pengajar...')

        instructor_group, _ = Group.objects.get_or_create(name='instructor')

        existing = set(
            User.objects.filter(username__startswith='dosen')
            .values_list('username', flat=True)
        )

        wib = pytz.timezone('Asia/Jakarta')
        now_wib = timezone.now().astimezone(wib)

        to_create = []
        for i in range(1, 21):
            username = f'dosen{i:02d}'
            if username not in existing:
                fname = FIRST_NAMES[(i - 1) % len(FIRST_NAMES)]
                lname = LAST_NAMES[(i - 1) % len(LAST_NAMES)]
                to_create.append(User(
                    username=username,
                    first_name=fname,
                    last_name=lname,
                    email=f'{username}@univ.ac.id',
                    is_staff=False,
                    password=make_password('dosen'),
                    date_joined=now_wib,
                    last_login=now_wib,
                ))

        if to_create:
            User.objects.bulk_create(to_create, ignore_conflicts=True)

        teachers = list(User.objects.filter(username__startswith='dosen'))
        for teacher in teachers:
            teacher.groups.add(instructor_group)

        self.stdout.write(f'  -> {len(teachers)} pengajar tersedia')
        return teachers

    def _seed_students(self):
        self.stdout.write('\n[2/6] Membuat mahasiswa ...')

        student_group, _ = Group.objects.get_or_create(name='student')

        existing = set(
            User.objects.filter(username__startswith='mhs')
            .values_list('username', flat=True)
        )

        wib = pytz.timezone('Asia/Jakarta')
        now_wib = timezone.now().astimezone(wib)

        to_create = []
        for i in range(1, 81):
            username = f'mhs{i:03d}'
            if username not in existing:
                to_create.append(User(
                    username=username,
                    first_name=random.choice(FIRST_NAMES),
                    last_name=random.choice(LAST_NAMES),
                    email=f'{username}@student.univ.ac.id',
                    password=make_password('mahasiswa'),
                    date_joined=now_wib,
                    last_login=now_wib,
                ))

        if to_create:
            User.objects.bulk_create(to_create, ignore_conflicts=True)

        students = list(User.objects.filter(username__startswith='mhs'))
        for student in students:
            student.groups.add(student_group)

        self.stdout.write(f'  -> {len(students)} mahasiswa yang tersedia')
        return students

    def _seed_courses(self, teachers):
        self.stdout.write('\n[3/6] Membuat 100 mata kuliah...')

        existing_count = Course.objects.count()
        to_create = []

        for i in range(existing_count, 100):
            subject = SUBJECTS[i % len(SUBJECTS)]
            kelas_idx = i // len(SUBJECTS)
            name = subject if kelas_idx == 0 else f'{subject} - Kelas {chr(65 + kelas_idx - 1)}'
            to_create.append(Course(
                name=name,
                description=(
                    f'Mata kuliah {subject} membahas konsep dasar hingga lanjutan '
                    f'dengan pendekatan teori dan praktikum. Mahasiswa akan mampu '
                    f'menerapkan ilmu ini di dunia kerja.'
                ),
                price=random.choice(PRICES),
                teacher=random.choice(teachers),
            ))

        if to_create:
            Course.objects.bulk_create(to_create, batch_size=500)

        courses = list(Course.objects.all()[:100])
        self.stdout.write(f'  -> {Course.objects.count()} mata kuliah yang tersedia')
        return courses

    def _seed_members(self, courses, students):
        self.stdout.write('\n[4/6] Membuat 500 anggota kelas...')

        existing_count = CourseMember.objects.count()
        existing_pairs = set(
            CourseMember.objects.values_list('course_id_id', 'user_id_id')
        )

        to_create = []
        attempts = 0
        target = 500 - existing_count

        while len(to_create) < target and attempts < 10000:
            attempts += 1
            course = random.choice(courses)
            student = random.choice(students)
            pair = (course.id, student.id)

            if pair not in existing_pairs:
                existing_pairs.add(pair)
                role = 'ast' if random.random() < 0.1 else 'std'
                to_create.append(CourseMember(
                    course_id=course,
                    user_id=student,
                    roles=role,
                ))

        if to_create:
            CourseMember.objects.bulk_create(to_create, batch_size=500, ignore_conflicts=True)

        members = list(CourseMember.objects.all())
        self.stdout.write(f'  -> {CourseMember.objects.count()} anggota kelas yang tersedia')
        return members

    def _seed_contents(self, courses):
        self.stdout.write('\n[5/6] Membuat 200 konten kelas...')

        existing_count = CourseContent.objects.count()
        to_create = []

        for i in range(existing_count, 300):
            course = courses[i % len(courses)]
            prefix = CONTENT_PREFIXES[i % len(CONTENT_PREFIXES)]
            topic = random.choice(CONTENT_TOPICS)
            to_create.append(CourseContent(
                name=f'{prefix} {topic}',
                description=(
                    f'Materi {prefix.lower()} mengenai {topic.lower()} '
                    f'dalam konteks {course.name}. '
                    f'Pelajari konsep ini dengan seksama dan sebelum mengerjakan latihan.'
                ),
                course_id=course,
                parent_id=None,
            ))

        if to_create:
            CourseContent.objects.bulk_create(to_create, batch_size=500)

        contents = list(CourseContent.objects.all()[:300])
        self.stdout.write(f'  -> {CourseContent.objects.count()} konten tersedia')
        return contents

    def _seed_comments(self, contents, members):
        self.stdout.write('\n[6/6] Membuat 100+ komentar...')

        existing_count = Comment.objects.count()
        target = 1000 - existing_count

        if target <= 0:
            self.stdout.write(f'  -> {Comment.objects.count()} komentar tersedia (skip)')
            return

        members_by_course = {}
        for member in members:
            cid = member.course_id_id
            if cid not in members_by_course:
                members_by_course[cid] = []
            members_by_course[cid].append(member)

        to_create = []
        fallback_members = members[:20]

        for _ in range(target):
            content = random.choice(contents)
            course_members = members_by_course.get(content.course_id_id, fallback_members)
            member = random.choice(course_members)
            to_create.append(Comment(
                content_id=content,
                member_id=member,
                comment=random.choice(COMMENTS),
            ))

        Comment.objects.bulk_create(to_create, batch_size=500)
        self.stdout.write(f'  -> {Comment.objects.count()} komentar tersedia')

    def _print_summary(self):
        self.stdout.write('')
        self.stdout.write(self.style.HTTP_INFO('-' * 60))
        self.stdout.write(self.style.HTTP_INFO('    Ringkasan Data'))
        self.stdout.write(self.style.HTTP_INFO('-' * 60))
        self.stdout.write(
            f"  User pengajar   : {User.objects.filter(username__startswith='dosen').count()}"
        )
        self.stdout.write(
            f"  User mahasiswa  : {User.objects.filter(username__startswith='mhs').count()}"
        )
        self.stdout.write(f'  Course          : {Course.objects.count()}')
        self.stdout.write(f'  CourseMember    : {CourseMember.objects.count()}')
        self.stdout.write(f'  CourseContent   : {CourseContent.objects.count()}')
        self.stdout.write(f'  Comment         : {Comment.objects.count()}')
        self.stdout.write(self.style.HTTP_INFO('-' * 60))