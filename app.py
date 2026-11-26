from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routes.upload import router as upload_router
from routes.visualize import router as visualize_router   # <-- ADD THIS

app = FastAPI(
    title="AI Data Visualization Assistant",
    version="1.0.0"
)

# Mount Static Folder
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# Templates Folder
templates = Jinja2Templates(directory="templates")

# Include Routes
app.include_router(upload_router)
app.include_router(visualize_router)   # <-- ADD THIS


# Home Page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )