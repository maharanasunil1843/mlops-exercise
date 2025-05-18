from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(
    filename="/app/logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
    )
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
MODEL_VERSION = os.getenv("MODEL_VERSION", "unknown")

# Initialize FastAPI app
app = FastAPI(title="Mock ML API")

# Pydantic model for request
class PredictionRequest(BaseModel):
	features: list[float]
 
# Welcome endpoint
@app.get("/")
async def welcome():
	return {"message": "Welcome to the Mock ML API! \n Use /predict to get predictions.\n Use /health to check the service health.\n Use /version to get the model version."}

# Mock prediction endpoint
@app.post("/predict")
async def predict(request: PredictionRequest):
	# Simulate ML prediction (e.g., sum of features)
	prediction = sum(request.features)
	# Log the prediction
	logger.info(f"Prediction made: {prediction} for features: {request.features}, Model version: {MODEL_VERSION}, Environment: {ENVIRONMENT}")
	# Return the prediction
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
