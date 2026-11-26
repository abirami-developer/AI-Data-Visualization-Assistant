from fastapi import APIRouter
from pydantic import BaseModel

from services.parser_service import ParserService
from services.file_service import FileService
from services.chart_service import ChartService
import routes.upload as upload

router = APIRouter()


class PromptRequest(BaseModel):
    prompt: str


@router.post("/visualize")
async def visualize(request: PromptRequest):

    if upload.CURRENT_FILE is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    df = FileService.read_dataset(upload.CURRENT_FILE)

    chart_info = ParserService.parse_prompt(
        request.prompt,
        df.columns.tolist()
    )

    fig = ChartService.generate_chart(
        df,
        chart_info
    )
    

    return {
    "success": True,
    "parsed_prompt": chart_info,
    "figure": fig.to_json()
    }