import loguru
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from elevenlabs import APIError
from uvicorn.server import Server
from uvicorn.config import Config
from src.voice_handler import main as voice_gen
from interface import Data
import src

__all__ = ["src"]

logger = loguru.logger

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/", tags=["voice_generation"])
def root(data: Data):
    """
    Endpoint for generating voice based on the received text and voice ID.

    Args:
        data (Data): The data object containing the text and voice ID.

    Returns:
        JSONResponse: The response object with the generated voice message.

    Raises:
        HTTPException: If the API request fails.
        APIError: If there is an error in the API request.

    """
    received_data: Data = data
    text = received_data.text
    voice_id = received_data.voice_id

    try:
        response = voice_gen(
            text=text, voice_id=voice_id, out_path="src/audio/in/input.txt"
        )
        return JSONResponse(status_code=200, content={"message": f"{response}"})
    except HTTPException as erorr:
        logger.exception(f"API request failed: \n{erorr}\n{text}\n{voice_id}")
        return JSONResponse(status_code=500, content={"error": str(erorr)})
    except APIError as erorr:
        logger.exception(f"API request failed: \n{erorr}\n{text}\n{voice_id}")
        return JSONResponse(status_code=401, content={"error": str(erorr)})


if __name__ == "__main__":
    server = Server(Config(app=app, host="localhost", port=8000, reload=True))
    server.run()
