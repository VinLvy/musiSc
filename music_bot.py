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
            print(f"Warning: File '{filename}' not found. Make sure it's in the '{music_folder}' directory.")
            time.sleep(1) 

    if not available_music:
        print(f"No music files found in '{music_folder}'. Please ensure you have your music files there.")
        return

    current_playing_info = "No music is currently playing."
    current_song_path = None # Stores the full path of the currently playing music file
    is_playing_looped = False 

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
                pygame.mixer.music.load(file_to_play)
                pygame.mixer.music.play(loops=-1) 
                is_playing_looped = True 
                current_playing_info = f"Playing (looping): {os.path.basename(current_song_path)}" # Display song name only
            else:
                current_playing_info = f"Invalid music number. Please select from the list.\n{current_playing_info}"
            
            clear_screen()
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
            continue 

        except ValueError:
            pass

        if user_input == "stop":
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                current_playing_info = "Music stopped."
                current_song_path = None
                is_playing_looped = False 
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
        
        clear_screen()
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

if __name__ == "__main__":
    music_player_bot()