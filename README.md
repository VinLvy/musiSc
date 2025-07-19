# musiSc

musiSc is a simple, console-based music player bot written in Python. It allows you to play local MP3 files directly from your terminal, offering basic controls like play, stop, pause, and resume. The bot provides a clean and interactive experience by dynamically updating its display.

## Features

- **Local Music Playback:** Plays audio files (e.g., MP3s) directly from your computer.

- **Dynamic Console Display:** Clears and refreshes the console screen to provide a clean, updated view of the current playing status and available commands.

- **Basic Controls:**

  - Select & Play: Just type the number of the song to play it.

  - Stop: Halts the current playback.

  - Pause: Temporarily stops the music.

  - Resume: Continues playback from where it was paused.

- **User-Friendly Interface:** Keeps the list of available songs and commands visible for easy interaction.

## Prerequisites

Before running musiSc, make sure you have the following installed:

- **Python 3.x:** Download from python.org.

- **Pygame:** A cross-platform set of Python modules designed for writing video games, which includes robust audio playback capabilities.

You can install Pygame using pip:

```Bash
pip install pygame
```
## Setup and Usage

1. **Save the Bot Script:**
Save the provided Python code as music_bot.py (or any other .py filename you prefer) in a directory of your choice.

2. **Prepare Your Music Files:**
Place your MP3 (or WAV, OGG) music files in the same directory as your music_bot.py script.

- Important: By default, the bot is configured to look for Any Other Way.mp3, Never Say Die.mp3, and A Moment Apart.mp3. You can rename your files to match these, or edit the music_files dictionary in the music_bot.py script to match your actual file names.

Example music_files dictionary in the code:

```Python
music_files = {
    "1": "Your Song Title 1.mp3",
    "2": "Another Great Song.mp3",
    "3": "Third Track.mp3"
}
```
4. **Run the Bot:**
Open your terminal or command prompt, navigate to the directory where you saved music_bot.py and your music files, and run the script:

```Bash
python music_bot.py
```

5. **Interact with the Bot:**
Follow the on-screen instructions. The bot will display a list of available songs by number and a list of commands.

<!-- ## Code Structure Highlights
clear_screen() function: Handles cross-platform console clearing (cls for Windows, clear for Linux/macOS) to enable dynamic display updates.

pygame.mixer: Utilized for robust audio loading, playing, pausing, and stopping.

music_files dictionary: Easily configurable to list your local music files and their corresponding selection numbers.

current_playing_info variable: Stores and updates the current status message (e.g., "Playing: Song Name") to be displayed persistently.

while True loop: The main bot loop continuously takes user input and manages command execution and display updates.

Troubleshooting
UserWarning: pkg_resources is deprecated...: This is a common warning from Pygame/Setuptools and does not affect the bot's functionality. You can safely ignore it.

"File 'filename' not found." Warning: Ensure your music files are in the same directory as music_bot.py, or update the file paths in the music_files dictionary within the script to their absolute locations.

No Sound: Double-check your system's audio output. Ensure Pygame is correctly installed.

Enjoy your simple console music player! -->