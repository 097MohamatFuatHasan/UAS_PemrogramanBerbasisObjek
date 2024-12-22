# UAS_PemrogramanBerbasisObjek!
[DagramClass](https://github.com/user-attachments/assets/0d3c6168-af9e-42a2-9fb2-6060cd7c37f6)
# Tile Game

## Diagram Kelas dan Struktur Kelas

### 1. Tile (Kelas Dasar)
Kelas `Tile` digunakan sebagai elemen dasar dari setiap blok dalam game.

#### Atribut:
- `value`: Nilai pada tile, seperti angka 2, 4, 8, dst.
- `position`: Posisi tile di dalam grid, direpresentasikan sebagai koordinat `(baris, kolom)`.

#### Metode Utama:
- `merge(other)`: Digunakan untuk menggabungkan dua tile dengan nilai yang sama. Setelah penggabungan, nilai tile akan menjadi dua kali lipat.
  - **Contoh:** Tile dengan nilai 2 digabungkan dengan tile lain yang bernilai 2, hasilnya tile bernilai 4.
- `render(screen, x, y)`: Menampilkan tile pada layar berdasarkan nilai dan posisinya.

### 2. PowerTile (Kelas Turunan dari Tile)
Kelas `PowerTile` memperluas fungsionalitas dari kelas `Tile` dengan menambahkan kemampuan khusus berupa "power".

#### Atribut Tambahan:
- `power`: Menyimpan nilai tambahan yang dapat meningkatkan kekuatan tile setiap kali tile digabungkan.

#### Modifikasi Metode:
- `merge(other)`: Selain menggandakan nilai tile seperti pada kelas induk, metode ini juga menambahkan nilai `power` setiap kali tile digabungkan.
- `render(screen, x, y)`: Sama seperti pada kelas `Tile`, tetapi ditambahkan tampilan nilai `power` sebagai elemen visual tambahan.

### 3. Grid
Kelas `Grid` bertanggung jawab untuk mengelola susunan tile di dalam grid permainan.

#### Atribut:
- `size`: Ukuran grid (4x4).
- `tiles`: Matriks dua dimensi untuk menyimpan semua tile di grid. Posisi yang belum terisi diwakili oleh `None`.

#### Fungsi Utama:
- `add_tile()`: Menambahkan tile baru di posisi kosong secara acak pada grid. Tile baru bisa berupa `Tile` biasa atau `PowerTile` dengan peluang tertentu.
- `slide(direction)`: Menggeser seluruh tile ke arah yang ditentukan pemain (atas, bawah, kiri, kanan). Jika ada tile dengan nilai yang sama berdekatan, mereka akan digabungkan.
- `is_game_over()`: Mengecek apakah permainan sudah berakhir. Kondisi akhir terjadi jika:
  - Tidak ada lagi ruang kosong di grid.
  - Tidak ada lagi tile yang dapat digabungkan.

### 4. Renderer
Kelas `Renderer` bertugas menggambar elemen permainan ke layar, termasuk grid dan tile.

#### Fungsi Utama:
- `render(grid)`: Menggambar seluruh grid permainan dan semua tile yang ada di dalamnya ke layar, termasuk menampilkan warna dan nilai masing-masing tile.

### 5. GameManager
Kelas `GameManager` adalah pengontrol utama yang mengatur seluruh alur permainan.

#### Atribut:
- `grid`: Objek dari kelas `Grid`, berfungsi untuk mengelola logika permainan.
- `renderer`: Objek dari kelas `Renderer`, digunakan untuk menggambar elemen permainan ke layar.
- `running`: Status permainan (berjalan atau tidak).

#### Fungsi Utama:
- `run()`:
  - Menangani input dari pemain (panah keyboard).
  - Memanggil metode pada grid untuk menggeser atau menggabungkan tile sesuai arah input.
  - Memperbarui tampilan layar menggunakan renderer.
  - Mengecek kondisi akhir permainan melalui `is_game_over()`.
- `display_game_over()`: Menampilkan pesan "Game Over" di layar setelah permainan selesai.

## Hubungan Antar Kelas

### Pewarisan:
- Kelas `PowerTile` mewarisi kelas `Tile`, sehingga memiliki semua atribut dan metode kelas induk, dengan tambahan fungsi spesifik.

### Komposisi:
- `GameManager` memiliki:
  - Objek dari kelas `Grid` untuk logika permainan.
  - Objek dari kelas `Renderer` untuk menggambar elemen ke layar.
- `Grid` berisi beberapa objek `Tile` dan `PowerTile`.

## Flowchart dan Alur Permainan

### Tahapan Permainan:

#### Inisialisasi:
1. Membuat grid ukuran 4x4 (16 posisi) menggunakan kelas `Grid`.
2. Menambahkan dua tile awal di posisi acak pada grid.

#### Input Pemain:
- Menunggu input pemain melalui tombol panah pada keyboard (atas, bawah, kiri, kanan).

#### Gerakan Tile:
1. Proses yang terjadi:
   - Tile digeser ke arah input.
   - Jika ada tile dengan nilai yang sama di jalur yang sama, mereka digabungkan.
2. Setelah setiap gerakan valid, tile baru akan ditambahkan secara acak.

#### Kondisi Akhir:
- Permainan dianggap selesai jika:
  - Tidak ada lagi posisi kosong pada grid.
  - Tidak ada lagi pasangan tile yang dapat digabungkan.
- Jika permainan selesai:
  - Pesan "Game Over" ditampilkan di layar.

---

**Selamat Bermain!**

