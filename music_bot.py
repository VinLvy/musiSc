import pygame
import os
import time
from mutagen.mp3 import MP3

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
            return os.path.basename(file_path)
    except Exception as e:
        return os.path.basename(file_path)

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
    pygame.display.set_mode((1, 1)) # Initialize a tiny, invisible display for event handling
    # Define a custom event for when a song ends
    SONG_END = pygame.USEREVENT + 1 # Custom event for end of song

    music_folder = "music_files"

    if not os.path.exists(music_folder):
        print(f"Error: Music folder '{music_folder}' not found. Please create it and put your music files inside.")
        return

    available_music_dict = {} # Dictionary for user selection (1, 2, 3...)
    playlist = [] # List for sequential playback
    track_number = 1
    # Iterate through files in the music_folder
    for filename in os.listdir(music_folder):
        file_path = os.path.join(music_folder, filename)
        # Check if it's a file and an MP3
        if os.path.isfile(file_path) and filename.lower().endswith('.mp3'):
            title = get_audio_title(file_path)
            duration = get_audio_duration(file_path)
            song_info = {"path": file_path, "title": title, "duration": duration}
            available_music_dict[str(track_number)] = song_info
            playlist.append(song_info) # Add to playlist
            track_number += 1

    if not available_music_dict:
        print(f"No music files found in '{music_folder}'. Please ensure you have your music files there.")
        return

    current_playing_info = "No music is currently playing."
    current_song_path = None
    is_playing_looped_single = False # True if a single song is looping
    is_playing_playlist = False # True if playing all songs in sequence
    current_playlist_index = -1 # Index of the current song in the playlist
    current_song_duration = 0

    # Initial display
    clear_screen()
    print("Hello! I am your local music player bot.")
    print("I can play music files from your computer.")
    print("\n--- Music Selection ---")
    for key, music_data in available_music_dict.items():
        formatted_duration = format_duration(music_data["duration"])
        print(f"{key}. {music_data['title']} ({formatted_duration})")
    print("-----------------------")
    print("Type the **number** of the music to play.")
    print("Type 'play all' to play all music in the folder.")
    print("Type 'stop' to stop the music")
    print("Type 'pause' to pause the music")
    print("Type 'resume' to resume the music")
    print("Type 'exit' to quit the bot")

    print("\n" + current_playing_info)

    while True:
        # --- Event Handling for Song End ---
        for event in pygame.event.get():
            if event.type == SONG_END:
                if is_playing_playlist and playlist:
                    current_playlist_index = (current_playlist_index + 1) % len(playlist)
                    next_song = playlist[current_playlist_index]
                    current_song_path = next_song["path"]
                    current_song_duration = next_song["duration"]
                    pygame.mixer.music.load(current_song_path)
                    pygame.mixer.music.play() # Play once, then signal end again
                    current_playing_info = f"Playing next: {next_song['title']}"
                    pygame.mixer.music.set_endevent(SONG_END) # Re-set event for next song
                elif is_playing_looped_single and current_song_path:
                    # This handles single song looping, but we already play with loops=-1 for single
                    # So this block is mostly for completeness if loop mode changes
                    pass # Handled by play(loops=-1) directly

        elapsed_time_str = ""

        # Re-display current playing info with duration if available
        # Find the title of the currently playing song for display
        current_display_title = "Unknown"
        if current_song_path:
            # Prefer title from playlist if in playlist mode
            if is_playing_playlist and current_playlist_index != -1:
                current_display_title = playlist[current_playlist_index]["title"]
            else: # Otherwise, find it from the dict (for single play)
                for key, music_data in available_music_dict.items():
                    if music_data["path"] == current_song_path:
                        current_display_title = music_data["title"]
                        break

        if "Playing" in current_playing_info or "Re-looping" in current_playing_info or "Resuming" in current_playing_info:
            status_prefix = "Playing (looping):" if is_playing_looped_single else ("Playing all:" if is_playing_playlist else "Playing:")
            current_playing_info_display = f"{status_prefix} {current_display_title}"
        elif "Paused" in current_playing_info:
            current_playing_info_display = f"Music paused: {current_display_title}"
        else:
            current_playing_info_display = current_playing_info

        clear_screen()
        print("Hello! I am your local music player bot.")
        print("I can play music files from your computer.")
        print("\n--- Music Selection ---")
        for key, music_data in available_music_dict.items():
            formatted_duration = format_duration(music_data["duration"])
            print(f"{key}. {music_data['title']} ({formatted_duration})")
        print("-----------------------")
        print("Type the **number** of the music to play.")
        print("Type 'play all' to play all music in the folder.")
        print("Type 'stop' to stop the music")
        print("Type 'pause' to pause the music")
        print("Type 'resume' to resume the music")
        print("Type 'exit' to quit the bot")

        print("\n" + current_playing_info_display)

        # Removed the old single-song re-looping logic
        # if current_song_path and is_playing_looped_single and not pygame.mixer.music.get_busy() and pygame.mixer.music.get_pos() == -1:
        #     pygame.mixer.music.load(current_song_path)
        #     pygame.mixer.music.play(loops=-1)
        #     relooping_title = "Unknown"
        #     for key, music_data in available_music_dict.items():
        #         if music_data["path"] == current_song_path:
        #             relooping_title = music_data["title"]
        #             break
        #     current_playing_info = f"Re-looping: {relooping_title}"

        user_input = input("\nYou: ").lower().strip()

        try:
            choice = str(int(user_input))
            if choice in available_music_dict:
                file_to_play_data = available_music_dict[choice]
                current_song_path = file_to_play_data["path"]
                current_song_duration = file_to_play_data["duration"]

                pygame.mixer.music.stop() # Stop any current playback
                is_playing_playlist = False # Exit playlist mode
                is_playing_looped_single = True # Enter single song loop mode
                current_playlist_index = -1 # Reset playlist index

                pygame.mixer.music.load(current_song_path)
                pygame.mixer.music.play(loops=-1) # Loop the selected single song indefinitely
                current_playing_info = f"Playing (looping): {file_to_play_data['title']}"
                pygame.mixer.music.set_endevent(0) # Disable end event for single song looping
            else:
                current_playing_info = f"Invalid music number. Please select from the list.\n{current_playing_info}"
            continue
        except ValueError:
            pass # Not a number, proceed to check other commands

        if user_input == "play all":
            if playlist:
                pygame.mixer.music.stop()
                is_playing_looped_single = False # Exit single song loop mode
                is_playing_playlist = True # Enter playlist mode
                current_playlist_index = 0 # Start from the first song

                first_song = playlist[current_playlist_index]
                current_song_path = first_song["path"]
                current_song_duration = first_song["duration"]

                pygame.mixer.music.load(current_song_path)
                pygame.mixer.music.play() # Play once
                current_playing_info = f"Playing all: {first_song['title']}"
                pygame.mixer.music.set_endevent(SONG_END) # Set event to trigger when song ends
            else:
                current_playing_info = "No music available to play all."
        elif user_input == "stop":
            if pygame.mixer.music.get_busy() or "Paused" in current_playing_info: # Check if music is playing or paused
                pygame.mixer.music.stop()
                current_playing_info = "Music stopped."
                current_song_path = None
                is_playing_looped_single = False
                is_playing_playlist = False
                current_playlist_index = -1
                current_song_duration = 0
                pygame.mixer.music.set_endevent(0) # Disable end event
            else:
                current_playing_info = "No music is currently playing."
        elif user_input == "pause":
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                current_playing_info = f"Music paused: {current_display_title}"
            else:
                current_playing_info = "No music is currently playing to pause."
        elif user_input == "resume":
            if pygame.mixer.music.get_pos() != -1 and not pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
                current_playing_info = f"Resuming: {current_display_title}"
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