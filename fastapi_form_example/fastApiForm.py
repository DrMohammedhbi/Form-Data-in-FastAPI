from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Point to the folder containing your HTML files
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    """Render the initial empty form."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit", response_class=HTMLResponse)
async def handle_form(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    role: str = Form(...),
    message: str = Form(""),  # Optional field with default empty string
):
    """Receive form data and re-render the page with a confirmation message."""
    submitted_data = {
        "username": username,
        "email": email,
        "role": role,
        "message": message,
    }
    return templates.TemplateResponse(
        "index.html", {"request": request, "submitted_data": submitted_data}
    )