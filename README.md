# 🛠️ Technical Math Solver

> **Aplikasi Edutainment Matematika & Teknik Terpadu (Divisi SMK)** > *Asisten perhitungan dan gambar teknik digital untuk siswa dan praktisi.*

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-green)
![Bootstrap](https://img.shields.io/badge/Frontend-Bootstrap%205-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📖 Tentang Aplikasi

**Technical Math Solver** adalah aplikasi berbasis web yang dikembangkan oleh **Kelompok 12 (TEKNIK)** untuk memenuhi tugas mata kuliah Pengembangan Aplikasi. Aplikasi ini dirancang khusus untuk membantu siswa SMK dan mahasiswa teknik dalam melakukan perhitungan matematis yang kompleks serta membuat sketsa gambar teknik standar secara digital.

Aplikasi ini menggabungkan antarmuka modern (Dashboard Style) dengan logika perhitungan fisika/matematika yang akurat.

---

## ✨ Fitur Utama

Aplikasi ini terdiri dari 5 modul utama yang terintegrasi:

### 1. ⚡ Kelistrikan (Electrical)
* **Hukum Ohm & Daya:** Menghitung Tegangan, Arus, Hambatan, dan Daya.
* **Rangkaian:** Analisis total hambatan/arus pada rangkaian Seri dan Paralel.

### 2. 📐 Geometri (Geometry)
* **Bangun Datar (2D):** Luas & Keliling (Persegi, Lingkaran, Trapesium, Layang-layang, dll).
* **Bangun Ruang (3D):** Volume & Luas Permukaan (Tabung, Kerucut, Bola, Prisma, dll).

### 3. 🔄 Konversi Unit (Conversion)
* Konversi universal untuk **10 Kategori Besaran**: Panjang, Massa, Suhu, Luas, Volume, Kecepatan, Tekanan, Daya, Energi, dan Waktu.

### 4. 🏗️ Material Teknik
* **Kalkulator Berat Material:** Menghitung berat logam berdasarkan bentuk profil (Plat, Pipa, As Bulat, As Kotak) dan massa jenis material (Baja, Aluminium, Beton, Kayu, dll).

### 5. ⚙️ Rekayasa Lanjut (Engineering Studio)
Ini adalah fitur unggulan (*Flagship Feature*) yang mencakup:
* **Mechanical Advantage:** Kalkulator Universal untuk Tuas, Katrol, Bidang Miring, dll. Menghitung AMA (Actual), IMA (Ideal), dan Efisiensi Mesin.
* **Structural Load:** Analisis Balok (*Beam Analysis*) untuk tumpuan sederhana & kantilever (Momen Maks, Geser, Lendutan/Deflection).
* **Fluid Dynamics:** Menghitung Debit Aliran, Bilangan Reynolds (Laminar/Turbulen), Tekanan Hidrostatis, dan Bernoulli.
* **✏️ Technical Drawing Helper (CAD Lite):**
    * Fitur sketsa berbasis vektor (Move/Edit Object).
    * *Building Outlines* (L-Shape, T-Shape, U-Shape Room).
    * *Openings* (Pintu Single/Double, Jendela Fixed/Sliding).
    * Ekspor gambar ke PNG dengan **Etiket Gambar (Title Block)** standar teknik otomatis.

---

## 💻 Teknologi yang Digunakan

* **Backend:** Python (Flask Framework).
* **Frontend:** HTML5, CSS3 (Custom Modern Dashboard), Bootstrap 5.
* **Scripting:** JavaScript Vanilla (Canvas API untuk fitur Drawing).
* **Database:** *Session-based* & In-memory storage (JSON logic).

---

## 🚀 Cara Instalasi & Menjalankan

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer lokal Anda:

1.  **Clone atau Download Repository**
    Pastikan Anda memiliki folder proyek ini di komputer Anda.

2.  **Siapkan Virtual Environment (Opsional tapi Disarankan)**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    Install library Flask yang dibutuhkan.
    ```bash
    pip install flask
    ```
    *(Atau jika ada file requirements.txt: `pip install -r requirements.txt`)*

4.  **Jalankan Aplikasi**
    ```bash
    python app.py
    ```

5.  **Buka di Browser**
    Akses alamat berikut di browser (Chrome/Edge/Firefox):
    `http://127.0.0.1:5000`

---

## 📂 Struktur Folder

```text
technical_math_solver/
│
├── app.py                # Logic Backend Utama
├── requirements.txt      # Daftar Library Python
├── static/
│   ├── modern.css        # Styling UI/UX Dashboard Modern
│   ├── drawing.js        # Logic Canvas CAD (Vector-based)
│   └── images/
│       └── qr-code.png   # QR Code Identitas Tim
└── templates/
    ├── base.html         # Layout Utama (Navbar & Footer)
    ├── index.html        # Dashboard Home
    ├── electric.html     # Modul Listrik
    ├── geometry.html     # Modul Geometri
    ├── conversion.html   # Modul Konversi
    ├── material.html     # Modul Material
    ├── engineering.html  # Modul Rekayasa (Tabbed Interface)
    └── team.html         # Halaman Profil Tim

## 👥 Tim Pengembang (Kelompok 12)
Proyek ini dikembangkan oleh mahasiswa Pendidikan Matematika, FKIP, Universitas Jember:

1. Tedy Bali Ragila (NIM: 24-071)
⭐ Full Stack Developer, Math & Technical Content, Project Manager

2. Ahmad Maulana Kafiyahya (NIM: 24-128)
⭐ Frontend Developer & Technical Developer

3. Anindya Fausta Adhidaiva Cetta (NIM: 24-041)
⭐ Mathematical Content Specialist

## 📝 Lisensi
Project ini dibuat untuk tujuan pendidikan. Silakan digunakan dan dikembangkan lebih lanjut.


Built with ❤️ for better technical education.
