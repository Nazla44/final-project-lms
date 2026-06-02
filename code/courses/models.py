"""
Models untuk App Courses

Perubahan dari lab sebelumnya:
- Course.instructor sekarang menyimpan user instruktur (rename dari teacher)
- Tambahan field: level, is_published
- CourseMember tetap ada untuk kompatibilitas
"""

from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner',     'Pemula'),
        ('intermediate', 'Menengah'),
        ('advanced',     'Lanjutan'),
    ]

    title       = models.CharField('Judul', max_length=200)
    description = models.TextField('Deskripsi', default='')
    price       = models.IntegerField('Harga', default=0)
    level       = models.CharField('Level', max_length=20, choices=LEVEL_CHOICES, default='beginner')
    image       = models.ImageField('Gambar', upload_to='courses/', null=True, blank=True)
    is_published = models.BooleanField('Dipublish', default=True)

    instructor  = models.ForeignKey(
        User,
        verbose_name='Instruktur',
        on_delete=models.RESTRICT,
        related_name='courses_taught'
    )

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name        = 'Mata Kuliah'
        verbose_name_plural = 'Mata Kuliah'
        ordering            = ['-created_at']
        indexes = [
            models.Index(fields=['price'],              name='idx_course_price'),
            models.Index(fields=['instructor', 'price'], name='idx_course_instructor_price'),
            models.Index(fields=['is_published'],        name='idx_course_published'),
        ]


class CourseContent(models.Model):
    title           = models.CharField('Judul', max_length=200)
    description     = models.TextField('Deskripsi', default='')
    video_url       = models.CharField('URL Video', max_length=500, null=True, blank=True)
    file_attachment = models.FileField('File', null=True, blank=True)
    order           = models.PositiveIntegerField('Urutan', default=0)

    course          = models.ForeignKey(
        Course,
        verbose_name='Kursus',
        on_delete=models.CASCADE,
        related_name='contents'
    )

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        verbose_name        = 'Konten Kursus'
        verbose_name_plural = 'Konten Kursus'
        ordering            = ['order']


ROLE_OPTIONS = [('std', 'Siswa'), ('ast', 'Asisten')]

class CourseMember(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.RESTRICT)
    user_id   = models.ForeignKey(User,   on_delete=models.RESTRICT)
    roles     = models.CharField(max_length=3, choices=ROLE_OPTIONS, default='std')

    class Meta:
        verbose_name        = 'Anggota Kelas'
        verbose_name_plural = 'Anggota Kelas'
