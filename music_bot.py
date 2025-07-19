import pygame
import os
import time # Meskipun tidak digunakan secara langsung untuk fungsionalitas utama, tetap dipertahankan jika ada penambahan fitur lain.

def music_player_bot():
    print("Halo! Saya adalah bot pemutar musik lokal Anda.")
    print("Saya bisa memutar musik dari file di komputer Anda.")

    # Inisialisasi Pygame Mixer
    pygame.mixer.init()

    # Lokasi file musik (pastikan file-file ini ada di direktori yang sama
    # atau berikan path absolutnya)
    music_files = {
        "1": "Any Other Way.mp3",
        "2": "Never Say Die.mp3",
        "3": "A Moment Apart.mp3"
    }

    # Periksa apakah file musik ada
    available_music = {}
    for key, filename in music_files.items():
        if os.path.exists(filename):
            available_music[key] = filename
        else:
            print(f"Peringatan: File '{filename}' tidak ditemukan.")

    if not available_music:
        print("Tidak ada file musik yang ditemukan. Pastikan Anda memiliki 'Any Other Way.mp3', 'Never Say Die.mp3', dll., di direktori yang sama.")
        return # Keluar jika tidak ada musik

    while True:
        print("\n--- Pilihan Musik ---")
        for key, filename in available_music.items():
            print(f"{key}. {filename}")
        print("---------------------")
        print("Cukup ketik **nomor** musik untuk memutar.")
        print("Ketik 'stop' untuk menghentikan musik")
        print("Ketik 'jeda' untuk menjeda musik")
        print("Ketik 'lanjut' untuk melanjutkan musik")
        print("Ketik 'daftar' untuk melihat daftar musik lagi")
        print("Ketik 'keluar' untuk mengakhiri bot")

        user_input = input("Anda: ").lower().strip()

        # Coba konversi input ke integer (untuk memilih musik)
        try:
            choice = str(int(user_input)) # Konversi ke int lalu kembali ke string untuk pencarian di dictionary
            if choice in available_music:
                file_to_play = available_music[choice]
                print(f"Memutar: {file_to_play}")
                pygame.mixer.music.load(file_to_play)
                pygame.mixer.music.play()
                continue # Lanjutkan ke iterasi berikutnya setelah memutar musik
            else:
                # Jika input adalah angka tapi bukan nomor musik yang tersedia
                print("Nomor musik tidak valid. Silakan pilih dari daftar.")
                continue
        except ValueError:
            # Jika input bukan angka, lanjutkan ke pengecekan perintah teks
            pass

        # Penanganan perintah teks
        if user_input == "stop":
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                print("Musik dihentikan.")
            else:
                print("Tidak ada musik yang sedang diputar.")
        elif user_input == "jeda":
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                print("Musik dijeda.")
            else:
                print("Tidak ada musik yang sedang diputar untuk dijeda.")
        elif user_input == "lanjut":
            # Periksa apakah musik dijeda (tidak 'busy' tapi bisa dilanjutkan)
            if pygame.mixer.music.get_pos() != -1 and not pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
                print("Musik dilanjutkan.")
            else:
                print("Musik sudah berjalan atau belum dijeda.")
        elif user_input == "daftar":
            pass # Loop akan mencetak daftar lagi secara otomatis
        elif user_input == "keluar":
            pygame.mixer.music.stop() # Hentikan musik sebelum keluar
            pygame.mixer.quit() # Hentikan mixer Pygame
            print("Bot: Sampai jumpa!")
            break
        else:
            print("Perintah tidak dikenal. Silakan coba lagi atau ketik nomor musik.")

if __name__ == "__main__":
    music_player_bot()