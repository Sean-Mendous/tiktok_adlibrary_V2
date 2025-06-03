from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.api.persona.logic import run_flow

app = FastAPI(root_path="/api/persona")

# CORSを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    input: dict

@app.post("/")
def persona_api(req: PromptRequest):
    try:
        result = run_flow(req.input)
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})

    return JSONResponse(status_code=200, content={"success": True, "data": result})


#activate fastapi
"""
uvicorn app.api.persona.main:app --host 0.0.0.0 --port 8000
"""