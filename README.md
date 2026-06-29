# Simple LMS - Final Project
## Identitas Mahasiswa

- **Nama:** Nazla Lutfia Ramadhani
- **NIM:** A11.2023.15259
- **Kelas:** A11.4618
- **Repository:** https://github.com/Nazla44/final-project-lms.git

---

## Overview

Simple LMS merupakan aplikasi Learning Management System (LMS) berbasis web yang dibangun menggunakan Django Rest Framework. Sistem ini dikembangkan untuk mengelola proses pembelajaran digital mulai dari pengelolaan course, materi pembelajaran, enrollment mahasiswa, hingga pemantauan progress belajar.
Pada pengembangan lanjutan ini, sistem telah ditingkatkan dengan penerapan beberapa teknologi pendukung seperti Celery untuk asynchronous processing, RabbitMQ sebagai message broker, Redis sebagai caching system, serta MongoDB untuk menyimpan log aktivitas pengguna.
Implementasi background processing memungkinkan proses berat seperti pengiriman email, pembuatan sertifikat, dan pembuatan laporan berjalan di belakang layar sehingga request utama API tetap responsif. Sistem juga menerapkan pembagian hak akses berdasarkan role pengguna yaitu **Admin, Instructor, dan Student**.

---

# Struktur Data Utama

| Model | Deskripsi |
|-------|-----------|
| **User** | Menyimpan informasi pengguna sistem beserta role pengguna seperti Admin, Instructor, dan Student. |
| **Course** | Menyimpan data course yang tersedia seperti nama course, deskripsi, harga, serta instructor yang mengelola. |
| **CourseContent** | Menyimpan materi atau lesson yang menjadi bagian dari suatu course. |
| **CourseMember** | Mengelola hubungan antara mahasiswa dengan course yang diikuti melalui proses enrollment. |
| **CourseContentCompletion** | Menyimpan informasi progress pembelajaran mahasiswa berdasarkan materi yang telah diselesaikan. |
| **Comment** | Menyimpan komentar atau diskusi mahasiswa pada materi pembelajaran. |

---

# Teknologi yang Digunakan

| Teknologi | Fungsi |
|-----------|--------|
| Django REST Framework | Framework utama untuk membangun REST API |
| PostgreSQL | Database utama aplikasi |
| Docker Compose | Menjalankan seluruh service dalam container |
| Celery | Menjalankan background task secara asynchronous |
| RabbitMQ | Message broker untuk komunikasi Celery |
| Redis | Penyimpanan cache dan backend hasil task |
| MongoDB | Penyimpanan log aktivitas pengguna |
| Flower | Monitoring proses Celery worker |

---

# Fitur Async Processing & Notification

Implementasi fitur tambahan menggunakan Celery terdiri dari:

| No | Fitur | Penjelasan |
|----|-------|------------|
| 1 | Async Email Notification | Sistem mengirim email notifikasi seperti enrollment atau penyelesaian course melalui background task Celery sehingga tidak memperlambat response API. |
| 2 | Generate Certificate | Sertifikat penyelesaian course dibuat dalam bentuk PDF melalui proses asynchronous menggunakan ReportLab. |
| 3 | Export Course Report | Sistem dapat menghasilkan laporan data course dalam format CSV melalui Celery task. |
| 4 | Scheduled Task | Celery Beat menjalankan proses otomatis seperti pembaruan statistik course secara berkala. |
| 5 | Task Monitoring Endpoint | User dapat melihat status proses asynchronous melalui endpoint task status berdasarkan task ID. |
| 6 | Flower Monitoring | Dashboard Flower digunakan untuk melihat aktivitas worker Celery dan task yang sedang berjalan. |


## Cara Menjalankan Project

### 1. Clone Repository

```bash
git clone https://github.com/Nazla44/final-project-lms.git
```

### 2. Jalankan Docker Compose

```bash
docker compose up --build
```
```bash
 docker compose up -d
```

![Menjalankan docker ](/docs/docs-1.png)

### 3. Pastikan Container Berjalan

```bash
docker ps
```

![docker compose ps](/docs/docs-2.png)

### 4. Buat migration dahulu

```bash
docker compose exec app python manage.py makemigrations
```

![makemigrations](/docs/docs-3.png)

### 5. Jalankan migration

```bash
docker compose exec app python manage.py migrate
```

![migrate](/docs/docs-4.png)

Pada proses dokumentasi, output saat pertama kali menjalankan migration tidak terdokumentasi secara lengkap. Namun setelah dilakukan pengecekan menggunakan perintah:

```bash
docker compose exec app python manage.py showmigrations
```

![showmigrate](/docs/docs-32.png)

seluruh migration telah berhasil, Hal ini menunjukkan bahwa seluruh struktur database seperti user, course, lesson, enrollment, dan komponen lainnya sudah berhasil dibuat dan database PostgreSQL telah tersinkronisasi dengan model Django.

### 6. Seed data

```bash
docker compose exec app python manage.py seed_data
```

![seed_data](/docs/docs-5.png)


## Akun Demo

![Akun Demo](/docs/docs-31.png)


## Endpoint Utama

  ### Authentication
  
  | Method | Endpoint             |
  | ------ | -------------------- |
  | POST   | `/api/auth/register` |
  | POST   | `/api/auth/login`    |
  | POST   | `/api/auth/refresh`  |
  | GET    | `/api/auth/me`       |
  | PUT    | `/api/auth/me`       |
  
  ### Courses
  
  | Method | Endpoint                     |
  | ------ | ---------------------------- |
  | GET    | `/api/courses`               |
  | POST   | `/api/courses`               |
  | GET    | `/api/courses/{id}`          |
  | PATCH  | `/api/courses/{id}`          |
  | DELETE | `/api/courses/{id}`          |
  | GET    | `/api/courses/{id}/contents` |
  | GET    | `/api/courses-cached`        |
  
  ### Enrollments
  
  | Method | Endpoint                         |
  | ------ | -------------------------------- |
  | POST   | `/api/enrollments`               |
  | GET    | `/api/enrollments/my-courses`    |
  | POST   | `/api/enrollments/{id}/progress` |
  
  ### Async Tasks 
  
  | Method | Endpoint                           |
  | ------ | ---------------------------------- |
  | POST   | `/api/enrollments-async`           |
  | POST   | `/api/courses/{id}/complete-async` |
  | POST   | `/api/courses/{id}/export-async`   |
  | POST   | `/api/admin/update-stats`          |
  | GET    | `/api/tasks/{task_id}`             |
  
  ### Analytics
  
  | Method | Endpoint                         |
  | ------ | -------------------------------- |
  | GET    | `/api/analytics/popular-courses` |
  | GET    | `/api/analytics/my-activities`   |
