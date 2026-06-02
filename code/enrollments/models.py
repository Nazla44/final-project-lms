"""
Models untuk App Enrollments

Enrollment   : catatan pendaftaran student ke course
LessonProgress: progres student per konten/lesson
"""

from django.db import models
from django.contrib.auth.models import User
from courses.models import Course, CourseContent


class Enrollment(models.Model):
    student    = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='enrollments', verbose_name='Siswa'
    )
    course     = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        related_name='enrollments', verbose_name='Kursus'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active   = models.BooleanField('Aktif', default=True)

    def __str__(self):
        return f"{self.student.username} → {self.course.title}"

    class Meta:
        verbose_name        = 'Pendaftaran'
        verbose_name_plural = 'Pendaftaran'
        unique_together     = ('student', 'course')   # satu student satu course max satu enrollment
        ordering            = ['-enrolled_at']


class LessonProgress(models.Model):
    enrollment  = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE,
        related_name='progress', verbose_name='Pendaftaran'
    )
    content     = models.ForeignKey(
        CourseContent, on_delete=models.CASCADE,
        related_name='progress', verbose_name='Konten'
    )
    is_complete  = models.BooleanField('Selesai', default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.enrollment} - {self.content.title}"

    class Meta:
        verbose_name        = 'Progres Lesson'
        verbose_name_plural = 'Progres Lesson'
        unique_together     = ('enrollment', 'content')
