import os
import loguru
from typing import Optional, List

from src.voice_gen import main as voice_gen
from src.voice_gen import api_requests, play_audio, change_voice
from src.process_text import save_chunks
from pydub import AudioSegment

CHUNK_SIZE = 1000

logger = loguru.logger


def main(
    text: Optional[str],
    voice_id: Optional[str],
    text_input_path: Optional[str] = "./src/audio/in/input.txt",
    out_path: Optional[str] = "./src/audio/out/",
):
    """
    Main function that generates voice audio from input text.

    Args:
        text (Optional[str]): The input text to convert to voice audio. Defaults to None.
        voice_id (Optional[str]): The ID of the voice to use for the audio generation. Defaults to None.
        text_input_path (Optional[str]): The path to the input text file. Defaults to "./src/audio/in/input.txt".
        out_path (Optional[str]): The path to the output directory. Defaults to "./src/audio/out/".

    Returns:
        str: The path to the generated audio file.
    """
    if not out_path:
        out_path = "./src/audio/out/"
    if not text and text_input_path:
        with open(text_input_path, "r", encoding="utf-8") as file:
            if path_content := file.read():
                text = path_content
    if not text:
        raise ValueError("Input text and input text file is empty")
    logger.info(f"Generating voice. Sample text: {text[:10]}")
    text_paths = save_chunks(text_input=text)
    response = None
    if len(text_paths) > 1:
        audio_paths = []
        for i, path in enumerate(text_paths):
            base_name = os.path.basename(path).split(".")[0]
            out_filename = f"src/audio/out/{base_name}{i}.mp3"
            with open(path, "r", encoding="utf-8") as file:
                text = file.read()
                response = api_requests(input_text=text, voice=voice_id)
                with open(out_filename, "wb", buffering=CHUNK_SIZE) as file:
                    file.write(response.content)
                    file.close()
                audio_paths.append(out_filename)
                if not response:
                    raise ValueError("API request failed")
        audio_files = combine_audio(audio_paths, out_path)
    else:
        audio_files = [voice_gen(text_input=text, voice_id_input=voice_id)]
    if not audio_files:
        raise ValueError("API request failed")
    out_file = "audio.mp3"
    segments = AudioSegment.empty()
    for file in audio_files:
        segments += AudioSegment.from_mp3(file)
        with open(out_file, "wb", buffering=CHUNK_SIZE) as file:
            file.write(segments.get_raw_data())
            file.close()
    play_audio(out_file)
    return out_file


def combine_audio(audio_paths: List[str], out_dir: str = "./src/audio/out"):
    """
    Combine multiple audio files into a single audio file.

    Args:
        audio_paths (List[str]): A list of file paths to the audio files that need to be combined.
        out_dir (str, optional): The directory where the combined audio file will be saved. Defaults to "./src/audio/out".

    Returns:
        str: The file path to the combined audio file.

    Raises:
        FileNotFoundError: If any of the audio files specified in `audio_paths` do not exist.
        ValueError: If `audio_paths` is empty.
    """
    audio_paths.sort()
    combined_audio = AudioSegment.empty()
    file_path = None
    for file in audio_paths:
        file_path = "src/audio/out/combined_chunks.mp3"
        audio = AudioSegment.from_mp3(file)
        combined_audio += audio
    combined_audio.export(file_path, format="mp3")
    logger.info(f"Saved combined audio to {file_path}")
    return file_path


def save_file(outname="audio.mp3", out_dir="./src/audio/out"):
    """
    Save the audio files in the given directory as a single audio file.

    Args:
        outname (str): The name of the output audio file. Defaults to "audio.mp3".
        out_dir (str): The directory where the audio files are located. Defaults to "./src/audio/out".

    Returns:
        str: The path of the saved audio file.
    """
    audio_files = os.listdir(out_dir)
    out_file = f"{out_dir}/{outname}"
    segements = AudioSegment.empty()
    for file in audio_files:
        segements += AudioSegment.from_mp3(f"{out_dir}/{file}")
    segements.export(out_file, format="mp3")
    return out_file


def change_voice_id(voice_id_input: str):
    """
    A function to change the voice ID.

    Args:
        voice_id_input (str): The input voice ID.

    Returns:
        None
    """
    response = change_voice(id_input=voice_id_input)
    logger.info(f"Changed voice to {response}")


if __name__ == "__main__":
    main(
        text=None,
        voice_id="EXAVITQu4vr4xnSDxMaL",
        text_input_path="./src/audio/in/input.txt",
        out_path="./src/audio/out/",
    )
