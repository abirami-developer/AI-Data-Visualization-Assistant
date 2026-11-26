import pandas as pd
from typing import Dict

class SchemaService:

    @staticmethod
    def extract_schema(df: pd.DataFrame) -> Dict:

        schema = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "data_types": df.dtypes.astype(str).to_dict()
        }

        return schema

    @staticmethod
    def preview_data(df: pd.DataFrame):

        return df.head().to_dict(orient="records")