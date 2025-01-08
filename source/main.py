from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend import conversation, embeddings

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class Prompt(BaseModel):
    message: str
    
@app.get("/")
async def root():
    try:
        return FileResponse('static/html/index.html')
    except:
        raise HTTPException(status_code=404, detail="File not found")
@app.get("/chat")
async def chat():
    try:
        return FileResponse('static/html/chat.html')
    except:
        raise HTTPException(status_code=404, detail="File not found")

@app.post("/conversation")
async def conversation_endpoint(prompt: Prompt):
    context = embeddings.generate_context(prompt.message)
    response = conversation.conversationAI(prompt.message, context)
    return {"response": response}
        