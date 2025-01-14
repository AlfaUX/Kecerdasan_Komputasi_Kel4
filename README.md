## 🌟 Panduan Menjalankan Program

### 🚀 Persiapan Awal
1. **Install semua dependensi** dengan menjalankan perintah berikut:
   ```bash
   pip install -r requirements.txt
   ```
   
   Jika terjadi error, Anda dapat menginstal dependensi secara manual satu per satu:
   ```bash
   pip install Flask
   pip install pyrebase4
   pip install numpy
   ```

2. **Jalankan program** menggunakan perintah berikut:
   ```bash
   python app.py
   ```

![Python](https://img.shields.io/badge/python-3.9-blue)

### 🔧 Mengatasi Error Saat Menjalankan Program

#### 1. Pastikan setuptools Terinstal
Setuptools diperlukan untuk mengelola instalasi paket Python. Pastikan setuptools terinstal atau diperbarui dengan menjalankan perintah berikut:
   ```bash
   pip install --upgrade setuptools
   ```

#### 2. Periksa Fungsi pip
Pastikan pip telah terinstal dan diperbarui ke versi terbaru:
   ```bash
   python -m ensurepip --upgrade
   pip install --upgrade pip
   ```

Jika masalah tetap terjadi, pastikan semua dependensi yang tercantum di `requirements.txt` telah berhasil terinstal dan kompatibel dengan versi Python yang digunakan.

