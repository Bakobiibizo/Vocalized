import os
import re
from typing import Iterator, List
import loguru

logger = loguru.logger


def stream_text_chunker(chunks: Iterator[str]) -> Iterator[str]:
    """
    Generates an iterator that chunks a stream of text based on a set of splitters.
    Currently not used but plans are to implement it in the future.

    Args:
        chunks (Iterator[str]): An iterator that yields chunks of text.

    Yields:
        Iterator[str]: An iterator that yields the chunked text.

    Returns:
        Iterator[str]: An iterator that yields the chunked text.
    """
    splitters = (".", ",", "?", "!", ";", ":", "—", "-", "(", ")", "[", "]", "}", " ")
    buffer = ""
    for text in chunks:
        if buffer.endswith(splitters):
            yield buffer if buffer.endswith(" ") else buffer + " "
            buffer = text
        elif text.startswith(splitters):
            output = buffer + text[0]
            yield output if output.endswith(" ") else output + " "
            buffer = text[1:]
        else:
            buffer += text
    if buffer != "":
        yield buffer + " "


def save_chunks(
    text_input: str, output_folder: str = "./src/audio/in", max_chunk_size: int = 500
) -> List[str]:
    """
    Save the given text input as audio chunks.

    :param text_input:
        The input text to be saved as audio chunks.

    :param output_folder:
        The folder where the audio chunks will be saved. Default is "./src/audio/in".

    :param max_chunk_size:
        The maximum size of each audio chunk in characters. Default is 500.

    :return:
        A list of paths to the saved audio chunks.
    """
    logger.info("Saving chunks")
    paragraphs = text_input.split("\n\n")
    splitters = r"[.?!;:—\-\(\)\[\]{}]"
    current_chunk = ""
    current_chunk_size = 0

    chunk_idx = 0
    chunk_paths = []
    for paragraph in paragraphs:
        chunks = re.split(splitters, paragraph)
        for chunk in chunks:
            chunk = chunk.strip()
            chunk_size = len(chunk)

            if current_chunk_size + chunk_size > max_chunk_size and current_chunk:
                filename = f"{output_folder}/chunk{chunk_idx}.txt"
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(current_chunk)
                logger.info(f"Saved chunk {chunk_idx} to {filename}")
                chunk_paths.append(filename)

                current_chunk = ""
                current_chunk_size = 0
                chunk_idx += 1

            if current_chunk:
                current_chunk += "\n\n"
            current_chunk += chunk
            current_chunk_size += chunk_size

    if current_chunk:
        filename = f"{output_folder}/chunk{chunk_idx}".replace(".txt", ".mp3")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(current_chunk)
        logger.info(f"Saved chunk {chunk_idx} to {filename}")
        chunk_paths.append(filename)
    return chunk_paths


def main(
    input_text: str, output_folder: str = "src/audio/in", max_chunk_size: int = 5000
):
    """
    Main function to process input text and save it in chunks to the output folder.

    :param input_text:
        The input text to be processed.

    :param output_folder:
        The folder path where the chunks will be saved. Default is "src/audio/in".

    :param max_chunk_size:
        The maximum size of each chunk. Default is 5000.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    save_chunks(
        text_input=input_text,
        output_folder=output_folder,
        max_chunk_size=max_chunk_size,
    )


if __name__ == "__main__":
    with open("src/audio/in/input.txt", "r", encoding="utf-8") as file:
        input_text = file.read()
    main(input_text=input_text)
