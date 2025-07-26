# MusiSc

MusiSc is a simple graphical music player built with Pygame in Python. It allows you to play local audio files through an intuitive windowed interface, offering essential controls and a clear display of your music library and current playback status.

## Features

- **Local Music Playback:** Plays audio files (e.g., MP3s, WAV, OGG) directly from your computer.

- **Graphical User Interface (GUI):** All interactions and displays are handled within a dedicated Pygame window, replacing the console-based output.

- **Automatic Playlist Progression:** When playing all songs, music automatically advances to the next track without manual intervention.

- **Playback Progress:** Displays the elapsed time and total duration for songs when playing a playlist.

- **Basic Controls:**

  - Select & Play: Type the number of the song to play it (loops a single song).

  - Play All: Plays all songs in the music_files folder sequentially.

  - Stop: Halts the current playback.

  - Pause: Temporarily stops the music.

  - Resume: Continues playback from where it was paused.

- **User-Friendly Interface:** Keeps the list of available songs and commands visible for easy interaction.

## Prerequisites

Before running MusiSc, make sure you have the following installed:

- **Python 3.x:** Download from python.org.

- **Pygame:** A cross-platform set of Python modules designed for writing video games, which includes robust audio playback capabilities.

- **mutagen:** A Python module to handle audio metadata (needed for getting audio duration).

You can install these libraries using pip:

```Bash
pip install pygame mutagen
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