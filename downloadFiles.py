from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from typing import List
import shutil
import os

# Create FastAPI instance
app = FastAPI()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
  os.makedirs(UPLOAD_DIR)

# Single file upload endpoint
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
  try:
      # Save uploaded file
      file_path = os.path.join(UPLOAD_DIR, file.filename)
      with open(file_path, "wb") as buffer:
          shutil.copyfileobj(file.file, buffer)
      
      return {
          "filename": file.filename,
          "status": "success",
          "message": f"File '{file.filename}' uploaded successfully"
      }
  except Exception as e:
      return {
          "status": "error",
          "message": f"Failed to upload file: {str(e)}"
      }

# Multiple files upload endpoint
@app.post("/upload-multiple/")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
  try:
      uploaded_files = []
      for file in files:
          file_path = os.path.join(UPLOAD_DIR, file.filename)
          with open(file_path, "wb") as buffer:
              shutil.copyfileobj(file.file, buffer)
          uploaded_files.append(file.filename)
      
      return {
          "filenames": uploaded_files,
          "status": "success",
          "message": f"Successfully uploaded {len(uploaded_files)} files"
      }
  except Exception as e:
      return {
          "status": "error",
          "message": f"Failed to upload files: {str(e)}"
      }

# File download endpoint
@app.get("/download/{filename}")
async def download_file(filename: str):
  file_path = os.path.join(UPLOAD_DIR, filename)
  
  if os.path.exists(file_path):
      return FileResponse(
          path=file_path,
          filename=filename,
          media_type='application/octet-stream'
      )
  return {
      "status": "error",
      "message": "File not found"
  }

# List all uploaded files
@app.get("/files/")
async def list_files():
  try:
      files = os.listdir(UPLOAD_DIR)
      return {
          "files": files,
          "status": "success",
          "count": len(files)
      }
  except Exception as e:
      return {
          "status": "error",
          "message": f"Failed to list files: {str(e)}"
      }

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)

# Created/Modified files during execution:
# - uploads/ (directory)
# - Any files uploaded through the API endpoints will be stored in the uploads/ directory