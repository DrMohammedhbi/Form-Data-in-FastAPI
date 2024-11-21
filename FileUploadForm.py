from fastapi import FastAPI,File,Form, UploadFile
app = FastAPI()
@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    description: str = Form(...)
):
    return {
        "filename": file.filename,
        "description": description
    }


