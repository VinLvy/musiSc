import pygame
import os
import time

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

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
            print(f"Warning: File '{filename}' not found.")
            time.sleep(1) # Give the user time to read the warning

    if not available_music:
        print("No music files found. Please ensure you have 'Any Other Way.mp3', 'Never Say Die.mp3', etc., in the same directory.")
        return

    current_playing_info = "No music is currently playing."
    current_song_name = None # Stores the name of the currently playing music file

    # Initial bot display
    clear_screen()
    print("Hello! I am your local music player bot.")
    print("I can play music files from your computer.")
    print("\n--- Music Selection ---")
    for key, filename in available_music.items():
        print(f"{key}. {filename}")
    print("-----------------------")
    print("Type the **number** of the music to play.")
    print("Type 'stop' to stop the music")
    print("Type 'pause' to pause the music")
    print("Type 'resume' to resume the music")
    # print("Type 'list' to show this music list again")
    print("Type 'exit' to quit the bot")

    print("\n" + current_playing_info) # Display initial status

    while True:
        user_input = input("\nYou: ").lower().strip() # Add a blank line so input doesn't stick

        # Try to convert input to an integer (for selecting music)
        try:
            choice = str(int(user_input))
            if choice in available_music:
                file_to_play = available_music[choice]
                current_song_name = file_to_play # Update the name of the playing song
                pygame.mixer.music.load(file_to_play)
                pygame.mixer.music.play()
                current_playing_info = f"Playing: {current_song_name}"
            else:
                current_playing_info = f"Invalid music number. Please select from the list.\n{current_playing_info}"
            
            # After processing input, clear the screen and reprint the status
            clear_screen()
            print("\n--- Music Selection ---")
            for key, filename in available_music.items():
                print(f"{key}. {filename}")
            print("-----------------------")
            print("Type the **number** of the music to play.")
            print("Type 'stop' to stop the music")
            print("Type 'pause' to pause the music")
            print("Type 'resume' to resume the music")
            # print("Type 'list' to show this music list again")
            print("Type 'exit' to quit the bot")

            print("\n" + current_playing_info)
            continue # Go back to the beginning of the loop for the next input

        except ValueError:
            # If the input is not a number, proceed to check for text commands
            pass

        # Handle text commands
        if user_input == "stop":
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                current_playing_info = "Music stopped."
                current_song_name = None
            else:
                current_playing_info = "No music is currently playing."
        elif user_input == "pause":
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                current_playing_info = f"Music paused: {current_song_name if current_song_name else 'Unknown'}"
            else:
                current_playing_info = "No music is currently playing to pause."
        elif user_input == "resume":
            if pygame.mixer.music.get_pos() != -1 and not pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
                current_playing_info = f"Resuming: {current_song_name if current_song_name else 'Unknown'}"
            else:
                current_playing_info = "Music is already playing or not paused."
        elif user_input == "list":
            # The "list" command will just trigger a screen refresh,
            # as the entire display is reprinted below.
            current_playing_info = "Music list displayed." # You can add this message
        elif user_input == "exit":
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            clear_screen() # Clear the screen one last time
            print("Bot: Goodbye!")
            break
        else:
            current_playing_info = f"Unknown command. Please try again or type a music number.\n{current_playing_info}"
        
        # Clear the screen and reprint the main display after any text command
        clear_screen()
        print("\n--- Music Selection ---")
        for key, filename in available_music.items():
            print(f"{key}. {filename}")
        print("-----------------------")
        print("Type the **number** of the music to play.")
        print("Type 'stop' to stop the music")
        print("Type 'pause' to pause the music")
        print("Type 'resume' to resume the music")
        # print("Type 'list' to show this music list again")
        print("Type 'exit' to quit the bot")

        print("\n" + current_playing_info)

if __name__ == "__main__":
    music_player_bot()