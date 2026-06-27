# Final Project Simple LMS Extended Backend 

## Identitas Mahasiswa

- **Nama:** Nazla Lutfia Ramadhani
- **NIM:** A11.2023.15259
- **Kelas:** A11.4618
- **Repository:** https://github.com/Nazla44/final-project-lms.git

---

## Deskripsi Project

Simple LMS adalah sistem manajemen pembelajaran berbasis Django REST Framework yang digunakan untuk mengelola course, lesson, enrollment, dan progress pengguna. Sistem ini menerapkan JWT Authentication, Role Based Access Control, serta asynchronous processing menggunakan Celery dan RabbitMQ untuk mendukung fitur seperti email notification, generate certificate/report, dan monitoring task melalui Flower.

---

## Fitur Dasar yang Sudah Berjalan

- Docker Compose Deployment, project dapat dijalankan menggunakan Docker Compose dengan seluruh servide yang dibutuhkan.
- Database PostgreSQL dan Migration, Sistem telah menggunakan PostgreSQL sebagai database utama untuk menyimpan data aplikasi. Struktur database dibuat menggunakan Django Migration sehingga pembuatan dan perubahan tabel dapat dikelola dengan baik.
- Authentication JWT, JWT digunakan untuk menjaga keamanan API dan memastikan hanya pengguna yang memiliki akses yang dapat menggunakan fitur tertentu.
- Role Based Access Control, pada sistem ini terdapat 3 role (Admin, Instructor, Student). Setiap Role memiliki batasan akses seduai dengan kebutuhan sistem.
- Fitur utama Learning Management System telah berjalan, meliputi Course Management, Lesson Management, Enrollment, dan Progress Tracking.
- Dokumentasi API Swagger/OpenAPI, Sistem menyediakan dokumentasi API menggunakan Swagger/OpenAPI sehingga seluruh endpoint dapat dilihat dan diuji secara langsung.
- Struktur Project dan Konfigurasi Environment, Struktur project telah dibuat secara terorganisir dengan memisahkan bagian aplikasi, konfigurasi, database, dan service tambahan.

---

## Fitur Tambahan yang Dipilih - SYNC PROCESSING & NOTIFICATION

| No  | Fitur                             | Fokus Implementasi                       | Poin | Status  |
| --- | --------------------------------- | ---------------------------------------- | ---- | ------- |
| 1   | Email notification async          | Email/mock email dikirim melalui Celery. | 12   | Selesai |
| 2   | Generate certificate/report async | Proses berat sebagai background task.    | 18   | Selesai |
| 3   | Scheduled task                    | Celery beat menjalankan task berkala.    | 15   | Selesai |
| 4   | Task status endpoint              | User mengecek status task                | 12   | Selesai |
| 5   | Flower monitoring                 | Monitoring Celery di Docker Compose      | 8    | Selesai |


---

## Penjelasan Implementasi - ASYNC PROCESSING & NOTIFICATION

Sistem menerapkan asynchronous processing menggunakan Celery sebagai pengelola background task dan RabbitMQ sebagai message broker. Implementasi ini digunakan untuk menjalankan proses yang membutuhkan waktu lama secara terpisah dari request utama API, sehingga aplikasi tetap responsif dan tidak perlu menunggu proses selesai.

### Email Notification Async

Fitur ini digunakan untuk mengirimkan email notifikasi secara asynchronous menggunakan Celery. Ketika user melakukan aktivitas seperti enrollment atau penyelesaian course, sistem akan membuat task pengiriman email yang diproses oleh Celery Worker tanpa menghambat response API.
Dengan metode ini, proses pengiriman email seperti welcome email, enrollment notification, dan completion email dapat berjalan di background sehingga aplikasi tetap memberikan response dengan cepat.

### Generate Certificate / Report Async

Fitur ini digunakan untuk membuat certificate PDF dan laporan CSV melalui background task. Proses generate file dipindahkan ke Celery Worker karena membutuhkan proses pengolahan data yang lebih besar. Ketika pengguna meminta pembuatan sertifikat atau laporan, sistem akan membuat task asynchronous dan hasil file akan disimpan setelah proses selesai. Hal ini membuat pengguna tidak perlu menunggu lama ketika menjalankan proses generate.

### Scheduled Task menggunakan Celery Beat

Celery Beat digunakan untuk menjalankan task secara otomatis berdasarkan jadwal tertentu. Fitur ini digunakan untuk proses berkala seperti update statistik course, pembersihan data sementara, atau pengiriman reminder belajar. Celery Beat akan mengirimkan task ke RabbitMQ sesuai jadwal, kemudian Celery Worker menjalankan proses tersebut secara otomatis.

### TASK STATUS ENDPOINT

Fitur ini memungkinkan pengguna mengecek status proses asynchronous menggunakan task_id yang diberikan setelah task dibuat. Endpoint ini menampilkan status proses seperti Pending, Started, Failed dan Success. Dengan fitur ini pengguna dapat mengetahui apakah proses seperti generate certificate atau report sudah selesai dijalankan.

### FLOWER MONITORING

Flower digunakan sebagai dashboard monitoring untuk memantau aktivitas Celery secara realtime. Melalui Flower, developer dapat melihat worker aktif, daftar task, status proses, serta task yang berhasil atau gagal.
Flower membantu proses monitoring dan debugging pada sistem asynchronous agar lebih mudah dilakukan.

### Kesimpulan

Implementasi Celery, RabbitMQ, dan Async Processing membuat sistem LMS mampu menjalankan proses berat secara background tanpa mengganggu performa aplikasi utama. Celery menangani eksekusi task, RabbitMQ mengatur antrean pesan, Celery Beat menjalankan task terjadwal, dan Flower digunakan untuk monitoring aktivitas asynchronous.

---

## Cara Menjalankan Project

### 1. Clone Repository

```bash
git clone https://github.com/Nazla44/final-project-lms.git
```

### 2. Jalankan Docker Compose
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

### 7. Akses Aplikasi

Django Admin Panel

```text
http://localhost:8000/admin/
```

![django Admin](/docs/docs-6.png)

Django Silk

```text
http://localhost:8000/silk/
```

![silk](/docs/docs-7.png)

Swagger:

```text
http://localhost:8000/api/docs/
```

![swanger](/docs/docs-8.png)

Flower :

```text
http://localhost:5555/
```

![flower](/docs/docs-9.png)

Rabbit MQ :

```text
http://localhost:15672/
```

![rabbitmq](/docs/docs-10.png)

---

## Akun Demo dan Endpoint Penting

![Akun Demo](/docs/docs-31.png)

## Screenshot / Bukti Pengujian

### Login API

![Login Admin](/docs/docs-13.png)
![Login Mahasiswa](/docs/docs-11.png)
![Login Dosen](/docs/docs-12.png)

### Email notification async

![Mahasiswa - Enroll Async](/docs/docs-14.png)
![Dosen - Enroll Async ](/docs/docs-15.png)
![Cek di Celery Berhasil](/docs/docs-16.png)
![Log Email Terkirim](/docs/docs-17.png)

### Generate certificate/report async

![Complete Course Mahasiswa (Generate Certificate)](/docs/docs-18.png)
![Cek Certificate di Celery Berhasil](/docs/docs-20.png)
![Cek File Certificate](/docs/docs-21.png)

![Export Complete](/docs/docs-22.png)
![Cek Exporty di Celery Berhasil](/docs/docs-23.png)
![Cek File report](/docs/docs-24.png)

### Scheduled task

![Log Celery Beat Berjalan](/docs/docs-25.png)
![Cek di Flower (Task SUCCESS)](/docs/docs-26.png)
![Detail Statistics](/docs/docs-27.png)

### TASK STATUS ENDPOINT

![Task Status Response](/docs/docs-28.png)

### Flower monitoring

![Flower Monitoring](/docs/docs-29.png)

### Rabbit MQ

![RabbitMQ Berjalan](/docs/docs-30.png)

## Kendala dan Solusi

### Kendala

- Database PostgreSQL tidak langsung memiliki tabel yang dibutuhkan setelah container berhasil dijalankan karena migration Django belum dijalankan di dalam container. Akibatnya beberapa endpoint seperti course, enrollment, dan progress mengalami error karena struktur tabel belum tersedia.
- File hasil generate certificate dan report tidak muncul pada folder media di host karena container Celery Worker belum memiliki volume mount yang mengarah ke folder media. Akibatnya file hanya tersimpan di dalam container sehingga tidak dapat diakses dari luar container.
- Implementasi Role Based Access Control mengalami kendala karena beberapa endpoint masih dapat diakses oleh role yang tidak sesuai. Hal ini terjadi karena permission pada Django REST Framework belum diterapkan secara konsisten pada setiap view.

### Solusi

- Menjalankan migration Django secara langsung di dalam container menggunakan perintah docker compose exec app python manage.py migrate, 
serta melakukan pengecekan menggunakan showmigrations untuk memastikan seluruh tabel berhasil dibuat
- Menambahkan volume mount pada service Celery Worker di docker-compose.yml seperti:
volumes:
  - ./documentation:/app/certificates
kemudian mengubah proses penyimpanan file menggunakan settings.MEDIA_ROOT agar hasil generate certificate dan report tersimpan pada folder media yang dapat diakses oleh host.
- Memperbaiki implementasi permission pada Django REST Framework dengan membuat custom permission berdasarkan role pengguna. Setiap endpoint kemudian diberikan aturan akses sesuai kebutuhan sistem seperti Admin, Instructor, dan Student.

## Kesimpulan

Project Simple Learning Management System (LMS) berhasil dikembangkan menggunakan Django REST Framework dengan dukungan Docker, PostgreSQL, JWT Authentication, Celery, dan RabbitMQ. Sistem telah menyediakan fitur utama seperti pengelolaan course, lesson, enrollment, dan progress dengan pembagian akses berdasarkan role pengguna.Selain fitur dasar, implementasi asynchronous processing menggunakan Celery dan RabbitMQ berhasil diterapkan untuk menangani proses seperti email notification, generate certificate/report, dan scheduled task sehingga aplikasi tetap responsif saat menjalankan proses berat. Secara keseluruhan, project ini berhasil menerapkan konsep sistem berbasis container dan background processing yang membuat aplikasi lebih terstruktur, scalable, dan mudah dikembangkan.




