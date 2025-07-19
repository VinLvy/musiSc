import pygame
import os
import time

def clear_screen():
    """Membersihkan layar konsol."""
    os.system('cls' if os.name == 'nt' else 'clear')

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
            time.sleep(1) # Beri waktu pengguna membaca peringatan

    if not available_music:
        print("Tidak ada file musik yang ditemukan. Pastikan Anda memiliki 'Any Other Way.mp3', 'Never Say Die.mp3', dll., di direktori yang sama.")
        return

    current_playing_info = "Tidak ada musik yang sedang diputar."
    current_song_name = None # Menyimpan nama file musik yang sedang diputar

    # Tampilan awal bot
    clear_screen()
    print("Halo! Saya adalah bot pemutar musik lokal Anda.")
    print("Saya bisa memutar musik dari file di komputer Anda.")
    print("\n--- Pilihan Musik ---")
    for key, filename in available_music.items():
        print(f"{key}. {filename}")
    print("---------------------")
    print("\n" + current_playing_info) # Tampilkan status awal
    print("Ketik **nomor** musik untuk memutar.")
    print("Ketik 'stop' untuk menghentikan musik")
    print("Ketik 'jeda' untuk menjeda musik")
    print("Ketik 'lanjut' untuk melanjutkan musik")
    print("Ketik 'daftar' untuk menampilkan daftar musik ini lagi")
    print("Ketik 'keluar' untuk mengakhiri bot")

    while True:
        user_input = input("\nAnda: ").lower().strip() # Tambahkan baris kosong agar input tidak menempel

        # Coba konversi input ke integer (untuk memilih musik)
        try:
            choice = str(int(user_input))
            if choice in available_music:
                file_to_play = available_music[choice]
                current_song_name = file_to_play # Update nama lagu yang sedang diputar
                pygame.mixer.music.load(file_to_play)
                pygame.mixer.music.play()
                current_playing_info = f"Memutar: {current_song_name}"
            else:
                current_playing_info = f"Nomor musik tidak valid. Silakan pilih dari daftar.\n{current_playing_info}"
            
            # Setelah memproses input, bersihkan layar dan cetak ulang status
            clear_screen()
            print("\n--- Pilihan Musik ---")
            for key, filename in available_music.items():
                print(f"{key}. {filename}")
            print("---------------------")
            print("\n" + current_playing_info)
            print("Ketik **nomor** musik untuk memutar.")
            print("Ketik 'stop' untuk menghentikan musik")
            print("Ketik 'jeda' untuk menjeda musik")
            print("Ketik 'lanjut' untuk melanjutkan musik")
            print("Ketik 'daftar' untuk menampilkan daftar musik ini lagi")
            print("Ketik 'keluar' untuk mengakhiri bot")
            continue # Kembali ke awal loop untuk input berikutnya

        except ValueError:
            # Jika input bukan angka, lanjutkan ke pengecekan perintah teks
            pass

        # Penanganan perintah teks
        if user_input == "stop":
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                current_playing_info = "Musik dihentikan."
                current_song_name = None
            else:
                current_playing_info = "Tidak ada musik yang sedang diputar."
        elif user_input == "jeda":
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                current_playing_info = f"Musik dijeda: {current_song_name if current_song_name else 'Tidak Diketahui'}"
            else:
                current_playing_info = "Tidak ada musik yang sedang diputar untuk dijeda."
        elif user_input == "lanjut":
            if pygame.mixer.music.get_pos() != -1 and not pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
                current_playing_info = f"Melanjutkan: {current_song_name if current_song_name else 'Tidak Diketahui'}"
            else:
                current_playing_info = "Musik sudah berjalan atau belum dijeda."
        elif user_input == "daftar":
            # Perintah "daftar" akan mencetak ulang seluruh tampilan,
            # sehingga mirip dengan cara kerja sebelumnya tetapi lebih terkontrol.
            current_playing_info = "Daftar musik ditampilkan." # Bisa tambahkan pesan ini
            # Tidak perlu tindakan khusus karena akan dicetak ulang di bawah
        elif user_input == "keluar":
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            clear_screen() # Bersihkan layar terakhir kali
            print("Bot: Sampai jumpa!")
            break
        else:
            current_playing_info = f"Perintah tidak dikenal. Silakan coba lagi atau ketik nomor musik.\n{current_playing_info}"
        
        # Bersihkan layar dan cetak ulang tampilan utama setelah setiap perintah teks
        clear_screen()
        print("\n--- Pilihan Musik ---")
        for key, filename in available_music.items():
            print(f"{key}. {filename}")
        print("---------------------")
        print("\n" + current_playing_info)
        print("Ketik **nomor** musik untuk memutar.")
        print("Ketik 'stop' untuk menghentikan musik")
        print("Ketik 'jeda' untuk menjeda musik")
        print("Ketik 'lanjut' untuk melanjutkan musik")
        print("Ketik 'daftar' untuk menampilkan daftar musik ini lagi")
        print("Ketik 'keluar' untuk mengakhiri bot")

if __name__ == "__main__":
    music_player_bot()