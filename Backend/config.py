# Configuration file for the API

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"
UPLOADS_DIR = BASE_DIR / "uploads"

# Create directories if they don't exist
UPLOADS_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# Model configuration
MODEL_PATH = MODELS_DIR / "best.pt"
MODEL_NAME = "YOLOv8m Fine-tuned"
MODEL_CONFIDENCE_DEFAULT = 0.25

# API configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
API_TITLE = "Safety Equipment Detection API"

# Class names mapping
CLASS_NAMES = {
    0: 'OxygenTank',
    1: 'NitrogenTank',
    2: 'FirstAidBox',
    3: 'FireAlarm',
    4: 'SafetySwitchPanel',
    5: 'EmergencyPhone',
    6: 'FireExtinguisher'
}

# Class colors for visualization
CLASS_COLORS = {
    'OxygenTank': '#FF0000',
    'NitrogenTank': '#00FF00',
    'FirstAidBox': '#0000FF',
    'FireAlarm': '#FFFF00',
    'SafetySwitchPanel': '#FF00FF',
    'EmergencyPhone': '#00FFFF',
    'FireExtinguisher': '#800080'
}

# Maximum file size (in MB)
MAX_FILE_SIZE_MB = 10

# Supported file extensions
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}

# Model performance metrics
MODEL_METRICS = {
    'mAP': 84.1,
    'precision': 0.85,
    'recall': 0.88,
    'inference_time_ms': 45  # Approximate
}
