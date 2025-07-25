import pygame
import os
import time
from mutagen.mp3 import MP3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
BLUE = (100, 100, 255)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# --- Helper functions (remain mostly the same) ---
def get_audio_duration(file_path):
    try:
        if file_path.lower().endswith(('.mp3', '.ogg', '.wav')): # Added common audio formats
            audio = MP3(file_path) # Mutagen supports MP3
            return audio.info.length
        else:
            return None
    except Exception as e:
        return None

def get_audio_title(file_path):
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
    if seconds is None:
        return "N/A"
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes:02}:{seconds:02}"

# --- Main Music Player GUI Function ---
def music_player_gui_bot():
    pygame.init()
    pygame.mixer.init()

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pygame Music Bot")

    # Fonts
    font_large = pygame.font.Font(None, 40) # For titles
    font_medium = pygame.font.Font(None, 30) # For song list
    font_small = pygame.font.Font(None, 25) # For status and input

    # Custom event for when a song ends
    SONG_END = pygame.USEREVENT + 1

    music_folder = "music_files"
    if not os.path.exists(music_folder):
        print(f"Error: Music folder '{music_folder}' not found. Please create it and put your music files inside.")
        # Render error on screen and wait for user to close
        error_text = font_medium.render(f"Error: Music folder '{music_folder}' not found.", True, WHITE)
        error_text2 = font_medium.render("Please create it and restart the bot.", True, WHITE)
        screen.fill(BLACK)
        screen.blit(error_text, (50, SCREEN_HEIGHT // 2 - 30))
        screen.blit(error_text2, (50, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            time.sleep(0.1) # Small delay to prevent high CPU usage in error state

    available_music_dict = {}
    playlist = []
    track_number = 1
    for filename in os.listdir(music_folder):
        file_path = os.path.join(music_folder, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(('.mp3', '.ogg', '.wav')):
            title = get_audio_title(file_path)
            duration = get_audio_duration(file_path)
            song_info = {"path": file_path, "title": title, "duration": duration}
            available_music_dict[str(track_number)] = song_info
            playlist.append(song_info)
            track_number += 1

    if not available_music_dict:
        print(f"No music files found in '{music_folder}'. Please ensure you have your music files there.")
        # Render error on screen and wait for user to close
        error_text = font_medium.render(f"No music files found in '{music_folder}'.", True, WHITE)
        error_text2 = font_medium.render("Please ensure you have your music files there.", True, WHITE)
        screen.fill(BLACK)
        screen.blit(error_text, (50, SCREEN_HEIGHT // 2 - 30))
        screen.blit(error_text2, (50, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            time.sleep(0.1)

    # --- Music playback state variables ---
    current_playing_info = "No music is currently playing."
    current_song_path = None
    is_playing_looped_single = False
    is_playing_playlist = False
    current_playlist_index = -1
    current_song_duration = 0

    # --- Input handling variables ---
    user_input_text = "" # What the user is currently typing
    input_active = True # Whether input is currently being accepted

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle song end event
            if event.type == SONG_END:
                if is_playing_playlist and playlist:
                    current_playlist_index = (current_playlist_index + 1) % len(playlist)
                    next_song = playlist[current_playlist_index]
                    current_song_path = next_song["path"]
                    current_song_duration = next_song["duration"]
                    pygame.mixer.music.load(current_song_path)
                    pygame.mixer.music.play()
                    current_playing_info = f"Playing next: {next_song['title']}"
                    pygame.mixer.music.set_endevent(SONG_END) # Re-set event for next song
                elif is_playing_looped_single:
                    pass # Already handled by loops=-1

            # Handle keyboard input
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN: # Enter key
                    command = user_input_text.strip().lower()
                    user_input_text = "" # Clear input after command

                    try:
                        choice = str(int(command))
                        if choice in available_music_dict:
                            file_to_play_data = available_music_dict[choice]
                            current_song_path = file_to_play_data["path"]
                            current_song_duration = file_to_play_data["duration"]

                            pygame.mixer.music.stop()
                            is_playing_playlist = False
                            is_playing_looped_single = True
                            current_playlist_index = -1

                            pygame.mixer.music.load(current_song_path)
                            pygame.mixer.music.play(loops=-1)
                            current_playing_info = f"Playing (looping): {file_to_play_data['title']}"
                            pygame.mixer.music.set_endevent(0)
                        else:
                            current_playing_info = f"Invalid music number. Please select from the list."
                    except ValueError:
                        # Not a number, check other commands
                        if command == "play all":
                            if playlist:
                                pygame.mixer.music.stop()
                                is_playing_looped_single = False
                                is_playing_playlist = True
                                current_playlist_index = 0

                                first_song = playlist[current_playlist_index]
                                current_song_path = first_song["path"]
                                current_song_duration = first_song["duration"]

                                pygame.mixer.music.load(current_song_path)
                                pygame.mixer.music.play() # Play once
                                current_playing_info = f"Playing all: {first_song['title']}"
                                pygame.mixer.music.set_endevent(SONG_END)
                            else:
                                current_playing_info = "No music available to play all."
                        elif command == "stop":
                            if pygame.mixer.music.get_busy() or "Paused" in current_playing_info:
                                pygame.mixer.music.stop()
                                current_playing_info = "Music stopped."
                                current_song_path = None
                                is_playing_looped_single = False
                                is_playing_playlist = False
                                current_playlist_index = -1
                                current_song_duration = 0
                                pygame.mixer.music.set_endevent(0)
                            else:
                                current_playing_info = "No music is currently playing."
                        elif command == "pause":
                            if pygame.mixer.music.get_busy():
                                pygame.mixer.music.pause()
                                current_playing_info = f"Music paused: {current_display_title}"
                            else:
                                current_playing_info = "No music is currently playing to pause."
                        elif command == "resume":
                            if pygame.mixer.music.get_pos() != -1 and not pygame.mixer.music.get_busy():
                                pygame.mixer.music.unpause()
                                current_playing_info = f"Resuming: {current_display_title}"
                            else:
                                current_playing_info = "Music is already playing or not paused."
                        elif command == "exit":
                            running = False # Set flag to exit the main loop
                        else:
                            current_playing_info = f"Unknown command: '{command}'"
                elif event.key == pygame.K_BACKSPACE:
                    user_input_text = user_input_text[:-1] # Remove last character
                else:
                    user_input_text += event.unicode # Add character to input string

        # --- Drawing everything on the Pygame window ---
        screen.fill(BLACK) # Clear the screen with black background

        # Title
        title_text = font_large.render("Pygame Music Bot", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 20))

        # Music Selection header
        music_header_text = font_medium.render("--- Music Selection ---", True, WHITE)
        screen.blit(music_header_text, (50, 70))

        # Display music list
        y_offset = 110
        for key, music_data in available_music_dict.items():
            formatted_duration = format_duration(music_data["duration"])
            song_line = f"{key}. {music_data['title']} ({formatted_duration})"
            
            # Highlight currently playing song
            if current_song_path and music_data["path"] == current_song_path:
                song_color = GREEN
            elif is_playing_playlist and current_playlist_index != -1 and playlist[current_playlist_index]["path"] == music_data["path"]:
                song_color = BLUE # Highlight current song in playlist mode
            else:
                song_color = WHITE
            
            song_text_surface = font_small.render(song_line, True, song_color)
            screen.blit(song_text_surface, (60, y_offset))
            y_offset += 25

        # Commands section
        commands_start_y = y_offset + 20
        commands_header_text = font_medium.render("--- Commands ---", True, WHITE)
        screen.blit(commands_header_text, (50, commands_start_y))
        
        command_list_y_offset = commands_start_y + 40
        commands_list = [
            "Type the **number** of the music to play.",
            "Type 'play all' to play all music in the folder.",
            "Type 'stop' to stop the music",
            "Type 'pause' to pause the music",
            "Type 'resume' to resume the music",
            "Type 'exit' to quit the bot"
        ]
        for cmd in commands_list:
            cmd_surface = font_small.render(cmd, True, WHITE)
            screen.blit(cmd_surface, (60, command_list_y_offset))
            command_list_y_offset += 25

        # Current playing info
        status_y = command_list_y_offset + 30
        current_display_title = "Unknown"
        if current_song_path:
            if is_playing_playlist and current_playlist_index != -1:
                current_display_title = playlist[current_playlist_index]["title"]
            else:
                for key, music_data in available_music_dict.items():
                    if music_data["path"] == current_song_path:
                        current_display_title = music_data["title"]
                        break

        if "Playing" in current_playing_info or "Re-looping" in current_playing_info or "Resuming" in current_playing_info:
            status_prefix = "Playing (looping):" if is_playing_looped_single else ("Playing all:" if is_playing_playlist else "Playing:")
            current_playing_info_display = f"{status_prefix} {current_display_title}"
            # Add current time if playing
            if pygame.mixer.music.get_busy() and current_song_duration:
                elapsed_ms = pygame.mixer.music.get_pos()
                elapsed_seconds = elapsed_ms / 1000
                current_time_str = format_duration(elapsed_seconds)
                total_duration_str = format_duration(current_song_duration)
                current_playing_info_display += f" ({current_time_str} / {total_duration_str})"
            
            status_color = GREEN if pygame.mixer.music.get_busy() else LIGHT_GRAY
        elif "Paused" in current_playing_info:
            current_playing_info_display = f"Music paused: {current_display_title}"
            status_color = BLUE
        else:
            current_playing_info_display = current_playing_info
            status_color = WHITE
            
        status_text_surface = font_medium.render(current_playing_info_display, True, status_color)
        screen.blit(status_text_surface, (50, status_y))

        # Input prompt and text box
        input_prompt_text = font_small.render("You: " + user_input_text + "|", True, WHITE) # Add '|' for cursor effect
        screen.blit(input_prompt_text, (50, SCREEN_HEIGHT - 50))

        # Update the full display
        pygame.display.flip()

        # Small delay to control frame rate and CPU usage
        pygame.time.Clock().tick(30) # Limit to 30 frames per second

    # Clean up Pygame resources when the main loop exits
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    pygame.quit() # Quits all pygame modules

if __name__ == "__main__":
    music_player_gui_bot()