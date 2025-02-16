# Alterkai Content Management

Aplikasi ini bertujuan untuk membantu admin dalam mengupload chapter ke container Azure, lalu mengembalikannya sebagai URL (seperti imagebox). Fitur seperti Database dengan SQLite juga direncanakan sebagai fitur kedepannya.

# Main System

1. main.py ===> Konversi gambar, rename, upload ke azure, beserta save ke database.
2. select.py ===> Retrieve gambar yang sudah diupload dalam bentuk img tag dari database.

Dibuat dua program terpisah agar admin bisa fokus entah upload terlebih dahulu baru fokus generate image tag kemudian. Ini juga membuat separation of concern, diharap memudahkan maintenance kedepannya.

# Tech/Language

Pyton 3.13.2


# Main Function

1. Konversi gambar ke webp, dengan kompresi sesuai konfigurasi
2. Rename file berdasarkan urutan logis
3. Upload ke Azure blob container
4. Save nama blob beserta chapter dan container ke SQLite
5. Generate URL img tag berdasarkan SQLite (not yet)