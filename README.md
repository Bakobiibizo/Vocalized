# Vocalized - Text to Speech Module

This is a simple api endpoint to communicate with the eleven labs api to generate speech from text. Run the server to setup the endpoint and ping it with your `text` and `voice_id` to generate and automatically play the audio.

## Overview

This project is designed to handle text-to-voice conversion using the Eleven Labs API. It includes functionalities to generate voice from text, combine audio files, save audio, and more. Currently only supports playback for windows, but linux support is coming soon.

### Installation

**Clone the Repository**:

`bash`
Copy code
`git clone [repository-link]`
Setup the Environment:

Windows: Run `install.bat`
Linux/Mac: Run `bash ./install.sh`

**Configure API Keys**:

Copy the `.example.env` file and rename it to `.env`.
Enter the required API keys for Eleven Labs in the `.env` file.
Usage
Running the Application
Windows: Run `run.bat`
Linux/Mac: Run `bash ./run.sh`

### API Endpoints

**root**: `/`
I just assigned this as root since there was no other endpoints. It accepts text a json object `data` with `text` as a string and `voice_id` as a string. You can get the voice_ids from the `voice_choices.json` file. I will be adding a selection option in the future.

**schema**: `
{
    "data":{
        "text":"Your text here",
        "voice_id":"this is optional"
    }
}
`

### Modules and Functions

**Text Processing**
process_text.py: Handles text processing, including chunking text streams and saving chunks as audio.

**Voice Generation**
voice_gen.py: Manages text-to-speech conversion, including changing voices, making API requests, and playing audio.

**Voice Handling**
voice_handler.py: Contains functions for generating voice audio, combining audio files, saving audio, and changing voice ID.

### Plans

This is a single module to a larger project I am working on. I plan to increase the functionality of this module to include local voice generation using Bark as well as linking it to the interface on the larger project to have adjustable variable inputs. For now it plays the audio I select and thats what I really needed in the short term. Let me know if you want anything added to it.

### Contributing

If you'd like to contribute send an email to [bakobiibizo@gmail.com] or make a pull request. This is a single piece of a larger project I am working on.

### License

[GNU General Public License v3.0](LICENSE)

### Acknowledgments

Eleven Labs: elevenlabs.io
Special thanks to Assistant(aka OpenAI's ChatGPT) for helping me debug, refine, and document the code.
