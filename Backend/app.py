from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from ultralytics import YOLO
import cv2
import numpy as np
import os
import shutil
from pathlib import Path
import uvicorn
from typing import List
import json
from datetime import datetime

app = FastAPI(title="Safety Equipment Detection API")

# CORS middleware (allow frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
# Change this path to where you place your downloaded model
MODEL_PATH = "models/best.pt"  # Place your best.pt in Backend/models/ folder
try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"Warning: Could not load model from {MODEL_PATH}. Error: {e}")
    print("Please ensure your trained model (best.pt) is in the 'models/' directory")
    model = None

# Create upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class_names = {
    0: 'OxygenTank',
    1: 'NitrogenTank',
    2: 'FirstAidBox',
    3: 'FireAlarm',
    4: 'SafetySwitchPanel',
    5: 'EmergencyPhone',
    6: 'FireExtinguisher'
}

@app.get("/")
def read_root():
    return {"message": "Safety Equipment Detection API", "status": "active"}

@app.get("/model-info")
def get_model_info():
    return {
        "model": "YOLOv8m Fine-tuned",
        "classes": len(model.names),
        "mAP": 84.1,
        "classes_list": class_names
    }

@app.post("/predict/single")
async def predict_single(
    file: UploadFile = File(...),
    confidence: float = 0.25
):
    """Predict single image"""
    try:
        # Save uploaded file
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        
        # Run prediction
        results = model.predict(file_location, conf=confidence)
        
        # Process results
        detections = []
        if results[0].boxes is not None:
            for box in results[0].boxes:
                cls_id = int(box.cls.item())  # Use .item() to extract scalar
                conf = float(box.conf.item())  # Use .item() to extract scalar
                bbox = box.xyxy.cpu().numpy()[0].tolist()
                
                detections.append({
                    "class": class_names.get(cls_id, f"Class_{cls_id}"),
                    "confidence": round(conf, 3),
                    "bbox": [int(x) for x in bbox],
                    "class_id": cls_id
                })
        
        # Create annotated image
        annotated_img = results[0].plot()
        
        # Fix image format - convert BGR to RGB if needed
        if annotated_img is not None:
            # annotated_img is already in BGR format from YOLO
            output_path = f"{UPLOAD_DIR}/annotated_{file.filename}"
            success = cv2.imwrite(output_path, annotated_img)
            
            if not success:
                # If cv2.imwrite fails, try alternative method
                from PIL import Image
                img_rgb = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(img_rgb)
                pil_img.save(output_path)
        else:
            output_path = file_location
        
        return {
            "filename": file.filename,
            "detections_count": len(detections),
            "detections": detections,
            "annotated_image": f"/download/{output_path}",
            "confidence_threshold": confidence,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        import traceback
        print(f"Error in predict_single: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/batch")
async def predict_batch(
    files: List[UploadFile] = File(...),
    confidence: float = 0.25
):
    """Predict multiple images"""
    try:
        batch_results = []
        
        for file in files:
            # Save file
            file_location = f"{UPLOAD_DIR}/{file.filename}"
            with open(file_location, "wb+") as file_object:
                shutil.copyfileobj(file.file, file_object)
            
            # Predict
            results = model.predict(file_location, conf=confidence)
            
            # Process
            detections = []
            if results[0].boxes is not None:
                for box in results[0].boxes:
                    cls_id = int(box.cls.item())  # Use .item() to extract scalar
                    conf = float(box.conf.item())  # Use .item() to extract scalar
                    
                    detections.append({
                        "class": class_names.get(cls_id, f"Class_{cls_id}"),
                        "confidence": round(conf, 3),
                        "class_id": cls_id
                    })
            
            # Count by class
            class_counts = {}
            for det in detections:
                class_name = det["class"]
                class_counts[class_name] = class_counts.get(class_name, 0) + 1
            
            batch_results.append({
                "filename": file.filename,
                "detections_count": len(detections),
                "class_counts": class_counts,
                "detections": detections[:5]  # First 5 detections
            })
        
        # Calculate batch statistics
        total_images = len(batch_results)
        total_detections = sum(r["detections_count"] for r in batch_results)
        
        return {
            "batch_id": f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "total_images": total_images,
            "total_detections": total_detections,
            "avg_detections_per_image": round(total_detections / max(total_images, 1), 2),
            "images": batch_results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        import traceback
        print(f"Error in predict_batch: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{file_path:path}")
async def download_file(file_path: str):
    """Serve annotated images"""
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": True}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)