# Depends : badal ma dal ektob object settins = settings() bkl file b3ayyetla marra bl depends
# UploadFile: lahetta a3mal upload lal file
# status : hon lahetta hadded eza good request or bad request ( 200 , 404 , ..)
from fastapi import FastAPI, APIRouter, Depends ,UploadFile , status

# response : 
from fastapi.responses import JSONResponse

from helpers.config import getSettings, Settings
from controllers import DataController, ProjectController
import os
import aiofiles
from models import ResponseSignal
import logging

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(

    prefix="/api/v1/data",
    tags = ["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(getSettings)):
    
    # Validate the file properties
    Is_Valid, Result = DataController().Validate(file=file)

    if not Is_Valid:
        return JSONResponse(
            # hayde ra2m l response ly baddo yreddo l file eza error mne5eda mn l status. 
            # (200 is good, 400 not good)
            status_code = status.HTTP_400_BAD_REQUEST,

            # content howwe shu badde red 
            content = {
                "signal" : Result,
            }

        )
    

    
    Project_dir_path = ProjectController().getProjectPath(project_id = project_id)
    file_path, file_id = DataController().Generate_Unique_FilePath(original_filename = file.filename,
                                                           project_id = project_id )
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)

    except Exception as e:
        # Hayde l log lal 5ata2 eza ana ma 3refet shu l error
        logger.error(f"Error while uploading file: {e}" )

        return JSONResponse(
            # hayde ra2m l response ly baddo yreddo l file eza error mne5eda mn l status. 
            # (200 is good, 400 not good)
            status_code = status.HTTP_400_BAD_REQUEST,

            # content howwe shu badde red 
            content = {
                "signal" : ResponseSignal.FILE_UPLOAD_FAILED.value,
            }

        )


    return JSONResponse(
        content = {
            "signal" : ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id" : file_id
        }
    )