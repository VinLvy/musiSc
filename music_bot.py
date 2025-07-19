import pygame
import os
import time

def music_player_bot():
    print("Halo! Saya adalah bot pemutar musik lokal Anda.")
    print("Saya bisa memutar musik dari file di komputer Anda.")

    pygame.mixer.init()

    music_files = {
        "1": "Any Other Way.mp3",
        "2": "Never Say Die.mp3",
        "3": "A Moment Apart.mp3"
    }

    available_music = {}
    for key, filename in music_files.items():
        if os.path.exists(filename):
            available_music[key] = filename
        else:
            print(f"Peringatan: File '{filename}' tidak ditemukan.")

    if not available_music:
        print("Tidak ada file musik yang ditemukan. Pastikan Anda memiliki 'Any Other Way.mp3', 'Never Say Die.mp3', dll., di direktori yang sama.")
        return

    while True:
        # Tampilan daftar musik dan instruksi selalu ditampilkan di awal setiap iterasi
        print("\n--- Pilihan Musik ---")
        for key, filename in available_music.items():
            print(f"{key}. {filename}")
        print("---------------------")
        print("Cukup ketik **nomor** musik untuk memutar.")
        print("Ketik 'stop' untuk menghentikan musik")
        print("Ketik 'jeda' untuk menjeda musik")
        print("Ketik 'lanjut' untuk melanjutkan musik")
        print("Ketik 'daftar' untuk melihat daftar ini lagi") # Perbarui instruksi
        print("Ketik 'keluar' untuk mengakhiri bot")

        user_input = input("Anda: ").lower().strip()

        # Coba konversi input ke integer (untuk memilih musik)
        try:
            choice = str(int(user_input))
            if choice in available_music:
                file_to_play = available_music[choice]
                print(f"Memutar: {file_to_play}")
                pygame.mixer.music.load(file_to_play)
                pygame.mixer.music.play()
                # Tidak perlu continue di sini karena loop akan otomatis mencetak ulang di awal
            else:
                print("Nomor musik tidak valid. Silakan pilih dari daftar.")
            continue # Penting: Langsung kembali ke awal loop setelah memproses pilihan angka
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
            if pygame.mixer.music.get_pos() != -1 and not pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
                print("Musik dilanjutkan.")
            else:
                print("Musik sudah berjalan atau belum dijeda.")
        elif user_input == "daftar":
            # Tidak perlu tindakan khusus karena loop akan mencetak ulang
            print("Mencetak daftar ulang...")
        elif user_input == "keluar":
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            print("Bot: Sampai jumpa!")
            break
        else:
            print("Perintah tidak dikenal. Silakan coba lagi atau ketik nomor musik.")
        
        # Penjelasan mengapa tidak ada 'continue' di sini:
        # Setelah setiap perintah teks selesai diproses, eksekusi secara alami
        # akan mencapai akhir loop 'while True' dan kemudian kembali ke awal loop,
        # yang akan mencetak ulang tampilan.

if __name__ == "__main__":
    music_player_bot()