import os
import pandas as pd
from fastapi import UploadFile


ALLOWED_EXTENSIONS = [".csv", ".json"]


class FileService:

    @staticmethod
    async def save_file(file: UploadFile, upload_folder: str) -> str:

        extension = os.path.splitext(file.filename)[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise ValueError("Only CSV and JSON files are allowed.")

        file_path = os.path.join(upload_folder, file.filename)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        return file_path

    @staticmethod
    def read_dataset(file_path: str) -> pd.DataFrame:

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".csv":
            return pd.read_csv(file_path)

        elif extension == ".json":
            return pd.read_json(file_path)

        else:
            raise ValueError("Unsupported file format.")