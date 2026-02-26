from fastapi import FastAPI, APIRouter, Depends
from helpers.config import getSettings, Settings
import os

base_router = APIRouter(

    prefix="/api/v1",
    tags = ["api_v1"],
)

@base_router.get("/")
async def welcome(app_settings: Settings = Depends(getSettings)):

#Depends : be5allene et2akad enno l getSettings jehze teshte8el w tjeb l value taba3a
    #app_settings = getSettings()

    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION

    return {
        "app_name" : app_name,
        "app_version" : app_version,
        #"message": "Hello world"
    }