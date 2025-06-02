import re
import json
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.llm.chatgpt_setting import chatgpt_4omini

app = FastAPI(root_path="/api")

# CORSを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#input
"""
{
 "target_info": {
   "age": “”,
   "gender": "",
   "why": "",
   "issue": ""
 },
 "product_info": {
   "category": "",
   "strength": "",
   "competition": "",
   "ideal": ""
 }
 "marketing_info": {
   "cost": "",
   "campaing": "",
   "apeals": ""
 }
}
"""

#output
"""
{
 "persona": {
   "name": "",
   "age": "",
   "gender": "",
   "residence": "",
   "lifestyle": "",
 },
 "insight": {
   "target_issue": [
	“”,
	“”,
	“”
   ],
   "product_solve": [
	“”,
	“”,
	“”
   ]
   "other_points":[
	“”,
	“”,
	“”
   ]
 }
}

"""

class PromptRequest(BaseModel):
    input: dict

@app.post("/persona")
def persona_api(req: PromptRequest):
    try:
        result = run_flow(req.input)
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})

    return JSONResponse(status_code=200, content={"success": True, "data": result})

def run_flow(input: str):
    try:
        prompt = create_prompt(input)
    except Exception as e:
        raise Exception(f"Error to create prompt: {e}")
    
    try:
        result = chatgpt_4omini(prompt)
    except Exception as e:
        raise Exception(f"Error to ask: {e}")
    
    try:
        converted_result = convert_to_dict(result)
    except Exception as e:
        raise Exception(f"Error to convert: {e}")
    
    return converted_result
    
def create_prompt(input: str):
    try:
        with open("app/api/persona/prompt.md", "r") as f:
            base_prompt = f.read()
        overall_prompt = f"{base_prompt}{input}"
        return overall_prompt
    except Exception as e:
        raise Exception(f"Error to create prompt: {e}")

def convert_to_dict(response):
    try:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", response)
        if match:
            json_str = match.group(1).strip()
        else:
            json_str = response.strip()
        if not json_str:
            raise ValueError("Empty JSON content after cleanup.")
        return json.loads(json_str)
    except Exception as e:
        raise Exception(f"Error to convert to dict: {e}")


#activate fastapi
"""
uvicorn app.api.persona.main:app --host 0.0.0.0 --port 8000
"""