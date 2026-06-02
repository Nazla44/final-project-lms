
import os
import logging
from celery import shared_task
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task(name="enrollments.tasks.send_enrollment_email")
def send_enrollment_email(user_id: int, course_id: int):
    """
    Async task untuk mengirim email konfirmasi enrollment ke student.
    """
    from django.contrib.auth.models import User
    from courses.models import Course

    try:
        user = User.objects.get(id=user_id)
        course = Course.objects.get(id=course_id)

        subject = f"Selamat! Kamu berhasil mendaftar ke {course.title}"
        body = (
            f"Halo {user.username},\n\n"
            f"Kamu telah berhasil mendaftar ke course:\n"
            f"Judul: {course.title}\n"
            f"Level: {course.get_level_display()}\n"
            f"Instruktur: {course.instructor.username}\n\n"
            f"Selamat belajar!\n\n"
            f"Tim LMS"
        )

        logger.info(f"[Email] TO: {user.email}")
        logger.info(f"[Email] SUBJECT: {subject}")
        logger.info(f"[Email] BODY:\n{body}")

        return {
            "status": "sent",
            "to": user.email,
            "subject": subject,
        }

    except Exception as exc:
        logger.error(f"[Email] Gagal mengirim email: {exc}")
        raise


@shared_task(name="enrollments.tasks.generate_certificate")
def generate_certificate(user_id: int, course_id: int):
    """
    Async task untuk generate sertifikat saat student menyelesaikan course.
    File disimpan ke folder media/certificates.
    """
    import time
    from django.contrib.auth.models import User
    from courses.models import Course
    from enrollments.models import Enrollment, LessonProgress
    from django.utils import timezone

    try:
        user = User.objects.get(id=user_id)
        course = Course.objects.get(id=course_id)
        enrollment = Enrollment.objects.get(student=user, course=course)

        total_contents = course.contents.count()
        completed_contents = LessonProgress.objects.filter(
            enrollment=enrollment,
            is_complete=True
        ).count()

        if total_contents == 0 or completed_contents < total_contents:
            logger.warning(
                f"[Certificate] {user.username} belum menyelesaikan semua lesson "
                f"({completed_contents}/{total_contents}) pada course {course.title}"
            )
            return {
                "status": "skipped",
                "reason": "Belum semua lesson selesai",
            }

        certificate_dir = os.path.join(settings.MEDIA_ROOT, "certificates")
        os.makedirs(certificate_dir, exist_ok=True)

        timestamp = int(time.time())
        filename = f"certificate_{course_id}_{user_id}_{timestamp}.pdf"
        filepath = os.path.join(certificate_dir, filename)

        issued_at = timezone.now().strftime("%d %B %Y %H:%M")

        pdf_content = _build_simple_pdf(
            student=user.get_full_name() or user.username,
            course=course.title,
            instructor=course.instructor.get_full_name() or course.instructor.username,
            issued_at=issued_at,
        )

        with open(filepath, "wb") as file:
            file.write(pdf_content)

        logger.info(f"[Certificate] Sertifikat berhasil dibuat: {filepath}")

        return {
            "status": "generated",
            "file": filepath,
            "filename": filename,
            "student": user.username,
            "course": course.title,
        }

    except Exception as exc:
        logger.error(f"[Certificate] Gagal membuat sertifikat: {exc}")
        raise


def _build_simple_pdf(student: str, course: str, instructor: str, issued_at: str) -> bytes:
    """
    Membuat file PDF sederhana tanpa library tambahan.
    """
    lines = [
        "SERTIFIKAT PENYELESAIAN KURSUS",
        "",
        "Diberikan kepada:",
        student,
        "",
        "Telah berhasil menyelesaikan kursus:",
        course,
        "",
        f"Instruktur: {instructor}",
        f"Tanggal: {issued_at}",
        "",
        "Simple LMS",
    ]

    y = 700
    text_stream = ""

    for line in lines:
        text_stream += f"BT /F1 14 Tf 72 {y} Td ({line}) Tj ET\n"
        y -= 24

    stream = text_stream.encode("latin-1", errors="replace")
    stream_len = len(stream)

    pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 842 595]\n"
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
        + f"4 0 obj\n<< /Length {stream_len} >>\nstream\n".encode()
        + stream
        + b"\nendstream\nendobj\n"
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
        b"xref\n0 6\n"
        b"0000000000 65535 f \n"
        b"0000000009 00000 n \n"
        b"0000000058 00000 n \n"
        b"0000000115 00000 n \n"
        b"0000000266 00000 n \n"
        b"0000000394 00000 n \n"
        b"trailer\n<< /Size 6 /Root 1 0 R >>\n"
        b"startxref\n459\n%%EOF\n"
    )

    return pdf