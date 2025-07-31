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

1. **Save the Player Script:**
Save the provided Python code as music_player.py (or any other .py filename you prefer) in a directory of your choice.

2. **Create Music Folder:**
In the same directory where you saved music_player.py, create a new folder named music_files.

3. **Place Your Music Files:**
Put your MP3 (or WAV, OGG) music files into the music_files folder. The player will automatically detect and list them.

Example music_files dictionary in the code:

```Python
music_files = {
    "1": "Your Song Title 1.mp3",
    "2": "Another Great Song.mp3",
    "3": "Third Track.mp3"
}
```
4. **Run the Player:**
Open your terminal or command prompt, navigate to the directory where you saved music_player.py, and run the script:

```Bash
python music_player.py
```

5. **Interact with the Player:**
A Pygame window will appear. Follow the on-screen instructions displayed in the window. The player will show a list of available songs by number and a list of commands you can type into the input area at the bottom.

## Troubleshooting

- **"Error: Music folder 'music_files' not found.":** Ensure you have created a folder named music_files in the same directory as your music_player.py script.

- **"No music files found in 'music_files'.":** Verify that your audio files (MP3, WAV, OGG) are correctly placed inside the music_files folder.

- **No Sound:** Double-check your system's audio output. Ensure Pygame is correctly installed (pip install pygame).

- **Window Not Responding:** Ensure pygame.display.flip() and pygame.time.Clock().tick(30) are present within your main loop to properly handle events and manage the frame rate.

Enjoy your simple graphical music player!

License
This project is licensed under the MIT License.