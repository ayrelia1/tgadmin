import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

load_dotenv()

current_directory = os.path.abspath(os.path.dirname(__file__))

app = FastAPI()
app.mount("/static", StaticFiles(directory=current_directory + "/static"), name="static")

templates = Jinja2Templates(directory=current_directory + "/templates")



class Settings(BaseSettings): # создаем settings class
    SESSION_EXPIRATION_TIME: int = int(os.getenv("SESSION_EXPIRATION_TIME", 3600))
    


settings = Settings()