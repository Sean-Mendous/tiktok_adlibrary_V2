from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.api.scene.logic import run_flow

app = FastAPI(
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    input: dict

@app.post("/persona")
def persona_api(req: PromptRequest):
    try:
        from app.api.persona.logic import run_flow
        result = run_flow(req.input)
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})

    return JSONResponse(status_code=200, content={"success": True, "data": result})

@app.post("/scene")
def scene_api(req: PromptRequest):
    try:
        from app.api.scene.logic import run_flow
        result = run_flow(req.input)
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})

    return JSONResponse(status_code=200, content={"success": True, "data": result})

#activate fastapi
"""
"""