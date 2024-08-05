import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from app.linkedin_tool import LinkedinTool
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
        title="LinkedIn Profile Agent",
        version="0.1.0",
    )

class ProfileRequest(BaseModel):
    profile_url: HttpUrl
    
class CompanyRequest(BaseModel):
    company_url: HttpUrl
    
api_key = os.getenv("PROXYCURL_API_KEY")
if not api_key:
    raise ValueError("PROXYCURL_API_KEY environment variable is not set")
tool = LinkedinTool(api_key)

@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/search/profile")
async def search_profile(request: ProfileRequest):
    try:
        profile_data = tool.search_profile(str(request.profile_url))
        return profile_data
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))

@app.post("/search/company")
async def search_company(request: CompanyRequest):
    try:
        company_data = tool.search_company(str(request.company_url))
        return company_data
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))