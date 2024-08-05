import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from dotenv import load_dotenv
from upstash_redis import Redis

from app.linkedin_tool import LinkedinTool

load_dotenv()

app = FastAPI(
        title="LinkedIn Profile Agent",
        version="0.1.0",
        servers=[
            {"url": "http://localhost:8000", "description": "Local Development Server"},
            {"url": "https://linkedin-profile-agent-e3a6e32ba353.herokuapp.com", "description": "Production Server"}
        ]
    )

class ProfileRequest(BaseModel):
    profile_url: HttpUrl
    
class CompanyRequest(BaseModel):
    company_url: HttpUrl
    
api_key = os.getenv("PROXYCURL_API_KEY")
if not api_key:
    raise ValueError("PROXYCURL_API_KEY environment variable is not set")
tool = LinkedinTool(api_key)

# Initialize Upstash Redis client
redis = Redis.from_env()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/search/profile")
async def search_profile(request: ProfileRequest):
    cache_key = f"profile:{request.profile_url}"
    cached_data = redis.get(cache_key)

    if cached_data:
        return json.loads(cached_data)

    try:
        profile_data = tool.search_profile(str(request.profile_url))
        
        redis.setex(cache_key, 604800, json.dumps(profile_data))  # Cache for 7 days
        
        return profile_data
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))

@app.post("/search/company")
async def search_company(request: CompanyRequest):
    cache_key = f"company:{request.company_url}"
    cached_data = redis.get(cache_key)

    if cached_data:
        return json.loads(cached_data)
    
    try:
        company_data = tool.search_company(str(request.company_url))
        
        redis.setex(cache_key, 604800, json.dumps(company_data))  # Cache for 7 days

        return company_data
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))