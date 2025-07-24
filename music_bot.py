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
        else:
            return None
    except Exception as e:
        # print(f"Error getting duration for {os.path.basename(file_path)}: {e}") # Optional: uncomment for debugging
        return None

def get_audio_title(file_path):
    """
    Gets the title of an audio file from its metadata.
    Supports MP3 files (ID3 tag 'TIT2').
    """
    try:
        if file_path.lower().endswith('.mp3'):
            audio = MP3(file_path)
            # 'TIT2' is the ID3 tag for the song title
            # .get('TIT2', [default_value]) returns a list, so take the first element [0]
            # If TIT2 tag is not present, it will default to the filename
            return audio.get('TIT2', [os.path.basename(file_path)])[0]
        else:
            return os.path.basename(file_path) # Return filename for unsupported types
    except Exception as e:
        # print(f"Error getting title for {os.path.basename(file_path)}: {e}") # Optional: uncomment for debugging
        return os.path.basename(file_path) # Fallback to filename if error occurs

def format_duration(seconds):
    """Formats duration from seconds into HH:MM:SS or MM:SS."""
    if seconds is None:
        return "N/A"
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

    available_music = {}
    track_number = 1
    # Iterate through files in the music_folder
    for filename in os.listdir(music_folder):
        file_path = os.path.join(music_folder, filename)
        # Check if it's a file and an MP3
        if os.path.isfile(file_path) and filename.lower().endswith('.mp3'):
            title = get_audio_title(file_path)
            duration = get_audio_duration(file_path)
            available_music[str(track_number)] = {"path": file_path, "title": title, "duration": duration}
            track_number += 1
        # else: # Optional: uncomment if you want to warn about non-MP3 files
        #     print(f"Skipping non-MP3 file: {filename}")


    if not available_music:
        print(f"No music files found in '{music_folder}'. Please ensure you have your music files there.")
        return

    current_playing_info = "No music is currently playing."
    current_song_path = None
    is_playing_looped = False
    current_song_duration = 0

    # Initial display
    clear_screen()
    print("Hello! I am your local music player bot.")
    print("I can play music files from your computer.")
    print("\n--- Music Selection ---")
    for key, music_data in available_music.items():
        formatted_duration = format_duration(music_data["duration"])
        print(f"{key}. {music_data['title']} ({formatted_duration})") # Display title and duration
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

        # Re-display current playing info with duration if available
        # Find the title of the currently playing song for display
        current_display_title = "Unknown"
        if current_song_path:
            for key, music_data in available_music.items():
                if music_data["path"] == current_song_path:
                    current_display_title = music_data["title"]
                    break

        if "Playing" in current_playing_info or "Re-looping" in current_playing_info or "Resuming" in current_playing_info:
            status_prefix = "Playing (looping):" if is_playing_looped else "Playing:"
            current_playing_info_display = f"{status_prefix} {current_display_title}"
        elif "Paused" in current_playing_info:
            current_playing_info_display = f"Music paused: {current_display_title}"
        else:
            current_playing_info_display = current_playing_info


        clear_screen()
        print("Hello! I am your local music player bot.")
        print("I can play music files from your computer.")
        print("\n--- Music Selection ---")
        for key, music_data in available_music.items():
            formatted_duration = format_duration(music_data["duration"])
            print(f"{key}. {music_data['title']} ({formatted_duration})") # Display title and duration
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
            # Update current_playing_info with the correct title
            relooping_title = "Unknown"
            for key, music_data in available_music.items():
                if music_data["path"] == current_song_path:
                    relooping_title = music_data["title"]
                    break
            current_playing_info = f"Re-looping: {relooping_title}"


        user_input = input("\nYou: ").lower().strip()

        try:
            choice = str(int(user_input))
            if choice in available_music:
                file_to_play_data = available_music[choice]
                current_song_path = file_to_play_data["path"]
                current_song_duration = file_to_play_data["duration"]
                pygame.mixer.music.load(current_song_path)
                pygame.mixer.music.play(loops=-1)
                is_playing_looped = True
                current_playing_info = f"Playing (looping): {file_to_play_data['title']}" # Use the title here
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
                current_song_duration = 0
            else:
                current_playing_info = "No music is currently playing."
        elif user_input == "pause":
            if pygame.mixer.music.get_busy():
                current_playing_info = f"Music paused: {current_display_title}" # Use current_display_title
            else:
                current_playing_info = "No music is currently playing to pause."
        elif user_input == "resume":
            if pygame.mixer.music.get_pos() != -1 and not pygame.mixer.music.get_busy():
                current_playing_info = f"Resuming: {current_display_title}" # Use current_display_title
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