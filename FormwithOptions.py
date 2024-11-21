from fastapi import FastAPI,Form
app = FastAPI()
@app.post("/profile/")
async def update_profile(
    username: str = Form(...),
    bio: str = Form(None),
    website: str = Form(None),
    age: int = Form(None)
):
    return {
        "username": username,
        "bio": bio,
        "website": website,
        "age": age
    }
