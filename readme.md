# Alterkai Upload Helper

Aplikasi ini bertujuan untuk membantu admin dalam mengupload chapter ke container Azure, lalu mengembalikannya sebagai URL (seperti imagebox)


# Tech/Language

Pyton 3.13.2


# Main Function

1. Konversi gambar ke webp, dengan kompresi sesuai konfigurasi

2. Rename file berdasarkan urutan logis

3. Upload ke Azure blob container

4. Save nama blob beserta chapter dan container ke SQLite

5. Generate URL img tag berdasarkan SQLite