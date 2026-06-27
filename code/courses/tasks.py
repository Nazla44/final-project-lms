from celery import shared_task
from django.core.mail import send_mail
from courses.permissions import get_role
from django.conf import settings
from django.utils import timezone
from io import StringIO
import csv
import os
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_enrollment_email(user_id, course_id, user_email, user_name, course_name):
    """Task 1: Kirim email saat student enroll"""
    try:
        subject = f"Selamat! Anda telah terdaftar di {course_name}"
        message = f"""
        Halo {user_name},
        
        Selamat! Anda berhasil terdaftar di course "{course_name}".
        
        Silakan mulai belajar di dashboard Anda.
        
        Terima kasih telah bergabung!
        """
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
        logger.info(f"Email sent to {user_email} for course {course_name}")
        return f"Email sent to {user_email}"
    except Exception as e:
        logger.error(f"Email failed: {e}")
        return None

@shared_task
def generate_certificate(user_id, course_id, user_name, course_name):
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader
        import os
        from django.conf import settings
        from django.utils import timezone
        from reportlab.lib import colors
        from reportlab.lib.units import cm

        cert_dir = os.path.join(settings.MEDIA_ROOT, 'certificates')
        os.makedirs(cert_dir, exist_ok=True)

        filename = f"certificate_{user_id}_{course_id}_{int(timezone.now().timestamp())}.pdf"
        filepath = os.path.join(cert_dir, filename)

        # Landscape A4
        c = canvas.Canvas(filepath, pagesize=landscape(A4))
        width, height = landscape(A4)

        # Background color
        c.setFillColorRGB(0.98, 0.95, 0.9)
        c.rect(0, 0, width, height, fill=1)

        # Border emas
        c.setStrokeColorRGB(0.8, 0.6, 0.2)
        c.setLineWidth(3)
        c.rect(50, 50, width-100, height-100)
        
        # Border dalam emas tipis
        c.setStrokeColorRGB(0.8, 0.6, 0.2)
        c.setLineWidth(1)
        c.rect(60, 60, width-120, height-120)

        # Title dengan shadow effect
        c.setFont("Helvetica-Bold", 36)
        c.setFillColorRGB(0.7, 0.5, 0.1)
        c.drawCentredString(width/2 + 2, height-100, "CERTIFICATE OF COMPLETION")
        c.setFillColorRGB(0.5, 0.3, 0.1)
        c.drawCentredString(width/2, height-98, "CERTIFICATE OF COMPLETION")

        # Subtitle
        c.setFont("Helvetica", 16)
        c.setFillColorRGB(0.3, 0.3, 0.3)
        c.drawCentredString(width/2, height-160, "This certificate is proudly presented to")

        # Nama User (lebih besar & warna biru)
        c.setFont("Helvetica-Bold", 32)
        c.setFillColorRGB(0.1, 0.3, 0.6)
        c.drawCentredString(width/2, height-240, user_name)

        # Teks
        c.setFont("Helvetica", 16)
        c.setFillColorRGB(0.2, 0.2, 0.2)
        c.drawCentredString(width/2, height-310, "for successfully completing the course")

        # Nama Course (lebih besar)
        c.setFont("Helvetica-Bold", 24)
        c.setFillColorRGB(0.5, 0.3, 0.1)
        c.drawCentredString(width/2, height-380, course_name)

        # Tanggal
        c.setFont("Helvetica", 12)
        c.setFillColorRGB(0.4, 0.4, 0.4)
        c.drawCentredString(width/2, height-480, f"Date: {timezone.now().strftime('%d %B %Y')}")

        # Footer
        c.setFont("Helvetica", 10)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawCentredString(width/2, height-540, "This certificate is valid and issued by the Learning Management System")

        c.save()
        return filepath
    except Exception as e:
        logger.error(f"Certificate generation failed: {str(e)}")
        return None
    
    
@shared_task
def update_course_statistics():
    """Task 3: Update enrollment count (scheduled task - setiap jam)"""
    from courses.models import Course, CourseMember

    results = []
    for course in Course.objects.all():
        count = CourseMember.objects.filter(course_id=course).count()
        results.append(f"Course {course.id} ({course.name}): {count} members")
        logger.info(f"Updated stat: {course.name} -> {count} members")

    return f"Updated {len(results)} courses: {', '.join(results[:5])}..."

@shared_task
def export_course_report(course_id, requester_email, course_name):
    """Task 4: Generate CSV report (async)"""
    from courses.models import CourseMember

    logger.info(f"Starting report export for course: {course_name}")

    
    report_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(report_dir, exist_ok=True)
    logger.info(f"Report directory: {report_dir}")

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['No', 'Username', 'Email', 'Role', 'Date Joined'])

    members = CourseMember.objects.filter(course_id=course_id).select_related('user_id')
    for idx, member in enumerate(members, 1):
        user = member.user_id
        writer.writerow([
            idx,
            user.username,
            user.email,
            get_role(user),
            timezone.localtime(user.date_joined).strftime('%Y-%m-%d %H:%M:%S') if user.date_joined else ''
        ])

    filename = f"report_course_{course_id}_{int(timezone.now().timestamp())}.csv"
    filepath = os.path.join(report_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(output.getvalue())

    if os.path.exists(filepath):
        file_size = os.path.getsize(filepath)
        logger.info(f" Report exported successfully! Size: {file_size} bytes")
    else:
        logger.error(f" Report file NOT FOUND after save: {filepath}")

    send_mail(
        f"Report for {course_name} is Ready",
        f"Report untuk course '{course_name}' telah siap. Download di: {settings.BASE_URL}/documentation/reports/{filename}",
        settings.DEFAULT_FROM_EMAIL,
        [requester_email]
    )

    logger.info(f"Report exported: {filepath}")
    return filename