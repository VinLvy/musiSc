import pygame
import os
import time
from mutagen.mp3 import MP3 # Import MP3 from mutagen

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_audio_duration(file_path):
    """
    Gets the duration of an audio file in seconds.
    Supports MP3 files.
    """
    try:
        if file_path.lower().endswith('.mp3'):
            audio = MP3(file_path)
            return audio.info.length
        # You can add support for other formats here if needed
        # elif file_path.lower().endswith('.wav'):
        #     import wave
        #     with wave.open(file_path, 'rb') as wf:
        #         frames = wf.getnframes()
        #         rate = wf.getframerate()
        #         duration = frames / float(rate)
        #         return duration
        else:
            return None # Or raise an error for unsupported formats
    except Exception as e:
        print(f"Error getting duration for {os.path.basename(file_path)}: {e}")
        return None

def format_duration(seconds):
    """Formats duration from seconds into HH:MM:SS or MM:SS."""
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes:02}:{seconds:02}"

def music_player_bot():
    print("Hello! I am your local music player bot.")
    print("I can play music files from your computer.")

    pygame.mixer.init()

    music_folder = "music_files"

    if not os.path.exists(music_folder):
        print(f"Error: Music folder '{music_folder}' not found. Please create it and put your music files inside.")
        return

    music_files = {
        "1": os.path.join(music_folder, "Any Other Way.mp3"),
        "2": os.path.join(music_folder, "Never Say Die.mp3"),
        "3": os.path.join(music_folder, "A Moment Apart.mp3")
    }

    available_music = {}
    for key, filename in music_files.items():
        if os.path.exists(filename):
            available_music[key] = filename
        else:
            print(f"Warning: File '{filename}' not found. Make sure it's in the '{music_folder}' directory.")
            time.sleep(1)

    if not available_music:
        print(f"No music files found in '{music_folder}'. Please ensure you have your music files there.")
        return

    current_playing_info = "No music is currently playing."
    current_song_path = None # Stores the full path of the currently playing music file
    is_playing_looped = False
    current_song_duration = 0 # To store the duration of the current song

    clear_screen()
    print("Hello! I am your local music player bot.")
    print("I can play music files from your computer.")
    print("\n--- Music Selection ---")
    for key, filename in available_music.items():
        print(f"{key}. {os.path.basename(filename)}")
    print("-----------------------")
    print("Type the **number** of the music to play.")
    print("Type 'stop' to stop the music")
    print("Type 'pause' to pause the music")
    print("Type 'resume' to resume the music")
    print("Type 'exit' to quit the bot")

    print("\n" + current_playing_info)

    while True:
        # Update elapsed time if music is playing
        elapsed_time_str = ""
        if pygame.mixer.music.get_busy() and current_song_path:
            elapsed_ms = pygame.mixer.music.get_pos()
            elapsed_seconds = elapsed_ms / 1000
            if current_song_duration:
                elapsed_time_str = f" [{format_duration(elapsed_seconds)} / {format_duration(current_song_duration)}]"
            else:
                elapsed_time_str = f" [{format_duration(elapsed_seconds)}]"

        # Re-display current playing info with duration if available
        if "Playing" in current_playing_info or "Re-looping" in current_playing_info or "Resuming" in current_playing_info:
            if current_song_path:
                song_name = os.path.basename(current_song_path)
                status_prefix = "Playing (looping):" if is_playing_looped else "Playing:"
                current_playing_info_display = f"{status_prefix} {song_name}{elapsed_time_str}"
            else:
                current_playing_info_display = current_playing_info
        elif "Paused" in current_playing_info:
            if current_song_path:
                song_name = os.path.basename(current_song_path)
                current_playing_info_display = f"Music paused: {song_name}{elapsed_time_str}"
            else:
                current_playing_info_display = current_playing_info
        else:
            current_playing_info_display = current_playing_info


        clear_screen()
        print("Hello! I am your local music player bot.")
        print("I can play music files from your computer.")
        print("\n--- Music Selection ---")
        for key, filename in available_music.items():
            print(f"{key}. {os.path.basename(filename)}")
        print("-----------------------")
        print("Type the **number** of the music to play.")
        print("Type 'stop' to stop the music")
        print("Type 'pause' to pause the music")
        print("Type 'resume' to resume the music")
        print("Type 'exit' to quit the bot")

        print("\n" + current_playing_info_display)


        # Check if music has finished playing and needs to be re-looped
        if current_song_path and is_playing_looped and not pygame.mixer.music.get_busy() and pygame.mixer.music.get_pos() == -1:
            pygame.mixer.music.load(current_song_path)
            pygame.mixer.music.play(loops=-1)
            current_playing_info = f"Re-looping: {os.path.basename(current_song_path)}" # Display song name only


        user_input = input("\nYou: ").lower().strip()

        try:
            choice = str(int(user_input))
            if choice in available_music:
                file_to_play = available_music[choice]
                current_song_path = file_to_play # Store the full path
                current_song_duration = get_audio_duration(file_to_play) # Get duration
                pygame.mixer.music.load(file_to_play)
                pygame.mixer.music.play(loops=-1)
                is_playing_looped = True
                current_playing_info = f"Playing (looping): {os.path.basename(current_song_path)}"
            else:
                current_playing_info = f"Invalid music number. Please select from the list.\n{current_playing_info}"

            continue

        except ValueError:
            pass

        if user_input == "stop":
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                current_playing_info = "Music stopped."
                current_song_path = None
                is_playing_looped = False
                current_song_duration = 0 # Reset duration
            else:
                current_playing_info = "No music is currently playing."
        elif user_input == "pause":
            if pygame.mixer.music.get_busy():
                current_song_display_name = os.path.basename(current_song_path) if current_song_path else 'Unknown'
                pygame.mixer.music.pause()
                current_playing_info = f"Music paused: {current_song_display_name}"
            else:
                current_playing_info = "No music is currently playing to pause."
        elif user_input == "resume":
            if pygame.mixer.music.get_pos() != -1 and not pygame.mixer.music.get_busy():
                current_song_display_name = os.path.basename(current_song_path) if current_song_path else 'Unknown'
                pygame.mixer.music.unpause()
                current_playing_info = f"Resuming: {current_song_display_name}"
            else:
                current_playing_info = "Music is already playing or not paused."
        elif user_input == "exit":
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            clear_screen()
            print("Bot: Goodbye!")
            break
        else:
            current_playing_info = f"Unknown command. Please try again or type a music number.\n{current_playing_info}"


if __name__ == "__main__":
    music_player_bot()