from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
import mysql.connector

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
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "secret")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "predictions")

# Initialize FastAPI app
app = FastAPI(title="Mock ML API")

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

# Create table for predictions (if not exists)
def create_predictions_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            features TEXT NOT NULL,
            prediction FLOAT NOT NULL,
            model_version VARCHAR(50),
            environment VARCHAR(50),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()

create_predictions_table()

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

    # Log the prediction to the file
    logger.info(f"Prediction made: {prediction} for features: {request.features}, Model version: {MODEL_VERSION}, Environment: {ENVIRONMENT}")

    # Log the prediction to the database
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO prediction_logs (features, prediction, model_version, environment)
        VALUES (%s, %s, %s, %s)
    """, (str(request.features), prediction, MODEL_VERSION, ENVIRONMENT))
    connection.commit()
    cursor.close()
    connection.close()

    # Return the prediction
    return {
        "prediction": prediction,
        "model_version": MODEL_VERSION,
        "environment": ENVIRONMENT
    }

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "model_version": MODEL_VERSION}

# Version check
@app.get("/version")
async def version():
    return {"model_version": MODEL_VERSION}
