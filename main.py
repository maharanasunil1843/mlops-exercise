from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
MODEL_VERSION = os.getenv("MODEL_VERSION", "unknown")

# Initialize FastAPI app
app = FastAPI(title="Mock ML API")

# Pydantic model for request
class PredictionRequest(BaseModel):
	features: list[float]

# Mock prediction endpoint
@app.post("/predict")
async def predict(request: PredictionRequest):
	# Simulate ML prediction (e.g., sum of features)
	prediction = sum(request.features)
	return {
		"prediction": prediction,
		"model_version": MODEL_VERSION,
		"environment": ENVIRONMENT
	}

# Health check
@app.get("/health")
async def health():
	return { "status": "healthy", "model_version": MODEL_VERSION}

# Version check
@app.get("/version")
async def version():
	return {"model_version": MODEL_VERSION}