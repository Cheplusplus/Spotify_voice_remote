
The purpose of this script is to provide a hands-free and convenient way to interact with Spotify without needing to manually operate the application. By speaking commands like "Pause," "Next," "Back," and so on, the script will translate those voice commands into appropriate calls to the Spotify API.

When the user speaks a command into the microphone, it captures the audio using Whisper and converts it into text. This transcription process allows the script to understand the command given by the user.

Once the command is transcribed, it checks the text to determine which action the user wants to perform. For example, if the user says "Pause," it recognises this as a command to pause the currently playing song. It then makes the corresponding API call to the Spotify API, instructing it to pause the playback.

Installation:

make a new directory to save the files
```
mkdir ~/spotify_voice_remote && cd ~/spotify_voice_remote
```

Clone the repository
```
git clone https://github.com/Cheplusplus/Spotify_voice_remote
```

Create a new virtual environment and activate it
```
mkdir venv && python3 -m venv venv && . venv/bin/activate
```

pip install all the requirements
```
pip install -r requirements.txt
```

Start the script
```
python3 Spotify_voice_remote.py
```

If you are having errors installing pyaudio try:
```
sudo apt-get install python3-dev build-essential portaudio19-dev
```

