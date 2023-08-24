import os
import argparse
import subprocess
import datetime
import requests
import loguru
from fastapi import HTTPException, Response
from typing import Optional
from dotenv import load_dotenv
from pydub import AudioSegment
import numpy as np
import simpleaudio as sa


CHUNK_SIZE = 1024
VOICE = "EXAVITQu4vr4xnSDxMaL"
logger = loguru.logger


def change_voice(id_input: str):
    """
    Change the voice for text-to-speech.

    Args:
        id_input (str): The ID of the voice to change to.

    Returns:
        str: A message indicating the voice has been changed.
    """
    global VOICE
    VOICE = id_input
    return f"Voice changed to {VOICE}"


def get_shell():
    """
    Get the default shell for the current user.

    :return: The name of the default shell for the current user (str) or None if an error occurred.
    """
    try:
        # Get the default shell for the current user
        shell_path = subprocess.getoutput("echo $SHELL")
        return shell_path.split("/")[-1]  # Extract the shell name from the path
    except OSError as err:
        print("An error while collecting shell name occurred:", err)
        return None


def api_requests(input_text: Optional[str] = None, voice: Optional[str] = None):
    """
    Makes an API request to convert text to speech using the Eleven Labs API.

    Args:
        input_text (Optional[str]): The input text to be converted to speech.
        voice (Optional[str]): The voice ID to be used for the speech conversion.

    Returns:
        requests.Response: The response object containing the API response.

    Raises:
        HTTPException: If the API request fails.

    """
    logger.info("Making API request")
    if not voice:
        voice = VOICE

    if not input_text:
        with open(
            "./src/audio/in/input.txt",
            "r",
            encoding="utf-8",
        ) as file:
            input_text = file.read()
    text_to_speech = input_text

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/stream"

    payload = {
        "text": f"{text_to_speech}",
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }
    load_dotenv()
    openai_api_key = os.getenv("ELEVEN_LABS_API_KEY")
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Insomnia/2023.5.2",
        "xi-api-key": f"{openai_api_key}",
        "Accept": "audio/mpeg",
    }
    logger.debug(headers)
    logger.debug(payload)
    try:
        resp: requests.Response = requests.request(
            "POST", url=url, json=payload, headers=headers, timeout=60
        )
        resp.raise_for_status()
    except requests.exceptions.RequestException as err:
        logger.error(f"API request failed: {err}")
        raise HTTPException(status_code=500, detail=str(err)) from err
    resp.content
    return resp


def play_audio(audio_path):
    """
    Plays an audio file.

    Args:
        audio_path (str): The path to the audio file.

    Returns:
        None
    """
    logger.info("Playing audio")
    audio_segment = AudioSegment.from_mp3(audio_path)

    samples = np.array(audio_segment.get_array_of_samples())
    samples = samples.astype(np.int16)

    play_obj = sa.play_buffer(samples, 1, 2, audio_segment.frame_rate)
    play_obj.wait_done()


def main(text_input: Optional[str] = None, voice_id_input: Optional[str] = None):
    """
    Generates a voice based on the given text input and voice ID.

    Args:
        text_input (Optional[str]): The input text to be converted to speech. Defaults to None.
        voice_id_input (Optional[str]): The ID of the voice to be used for the speech generation. Defaults to None.

    Returns:
        The response from the API request.

    Raises:
        ConnectionError: If the API request fails due to a connection error.
        OSError: If the API request fails due to an OS error.
    """
    logger.info("Starting voice generation")
    try:
        response = api_requests(voice=voice_id_input, input_text=text_input)
    except ConnectionError as error:
        raise ConnectionError(
            f"{logger.error(f'API request failed: {error}')}"
        ) from error
    try:
        date = datetime.date.today()
        entry = len(os.listdir("./src/audio/out"))
        audio_path = f"./src/audio/out/{date}_entry_{entry}.mp3"
        with open(audio_path, "wb", buffering=CHUNK_SIZE) as file:
            file.write(response.content)
            file.close()
        play_audio(audio_path)
        os.remove(audio_path)
    except OSError as error:
        raise OSError(f"{logger.error(f'API request failed: {error}')}") from error
    return response


def parse_args():
    """
    Parse the command line arguments and return the parsed arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    argparse.ArgumentParser(description="Text to speech")
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text", help="Text to be converted")
    parser.add_argument("-v", "--voice", help="Voice to be used")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    text = args.text
    voice_id = args.voice

    main(text_input=text, voice_id_input=voice_id)
