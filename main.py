from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
import httpx
from pydantic import StrictStr


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://api.genderize.io?name="


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    errors = exc.errors()

    for err in errors:
        if err["type"] == "missing":
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Query parameter 'name' is required"
                }
            )
        
        if "string" in err["type"]:
            return JSONResponse(
                status_code=422,
                content={
                    "status": "error",
                    "message": "Invalid type for 'name', expected string"
                    }
                )

@app.get("/api/classify")
async def classify_api(name: str = Query(..., min_length=1)):
    if not name.isalpha():
        return JSONResponse(
                status_code=422,
                content={
                    "status": "error",
                    "message": "Invalid type for 'name', expected string"
                    }
                )
    
    async with httpx.AsyncClient(timeout=2.0) as client:
        try:
            response = await client.get(BASE_URL + name)
            response.raise_for_status()
            data = response.json()

        except httpx.HTTPError as e:
            return JSONResponse(
                status_code=502,
                content={
                    "status": "error",
                    "message": "Failed to fetch data from Genderize API"
                }
            )

    gender =  data.get("gender")
    probability = data.get("probability")
    sample_size = data.get("count")

    if gender is None or sample_size == 0:
        return JSONResponse(
            status_code=200,
            content= { 
                "status": "error", 
                "message": "No prediction available for the provided name" 
                }
            )

    is_confident = (probability is not None and
                    probability >= 0.7 and
                    sample_size >= 100
                    )

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    result = {
        "status": "success",
        "data": {
            "name": name,
            "gender": gender,
            "probability": probability,
            "sample_size": sample_size,
            "is_confident": is_confident,
            "processed_at": timestamp
            }
}
    return JSONResponse(content=result, status_code=200)
