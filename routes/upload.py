import os

from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile
from fastapi import HTTPException

from services.file_service import FileService
from services.schema_service import SchemaService
from services.chart_service import ChartService

router = APIRouter()

UPLOAD_FOLDER = "uploads"

CURRENT_FILE = None


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):

    global CURRENT_FILE

    try:

        # Save uploaded file
        file_path = await FileService.save_file(
            file,
            UPLOAD_FOLDER
        )

        CURRENT_FILE = file_path

        # Read dataset
        df = FileService.read_dataset(file_path)

        # Extract dataset schema
        schema = SchemaService.extract_schema(df)

        # Generate dataset preview
        preview = SchemaService.preview_data(df)

        return {
            "message": "Dataset uploaded successfully.",
            "schema": schema,
            "preview": preview
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )