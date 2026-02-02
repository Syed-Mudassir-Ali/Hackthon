# Safety Equipment Detection System

A real-time object detection application for identifying safety equipment in industrial environments using YOLOv8 and FastAPI.

## Features

✅ **Single Image Detection** - Real-time detection on individual images
✅ **Batch Processing** - Process 1000+ images with automatic chunking (50-100 per chunk)
✅ **Class Detection** - Detect 7 safety equipment classes:
   - Oxygen Tank
   - Nitrogen Tank
   - First Aid Box
   - Fire Alarm
   - Safety Switch Panel
   - Emergency Phone
   - Fire Extinguisher

✅ **Web Interface** - Interactive frontend with drag-and-drop support
✅ **REST API** - Complete API for integration with other applications
✅ **High Accuracy** - 84.1% mAP with YOLOv8m fine-tuned model

## Project Structure

```
Hackthon/
├── Backend/
│   ├── app.py                 # FastAPI application
│   ├── config.py              # Configuration
│   ├── requirements.txt        # Python dependencies
│   ├── models/
│   │   └── best.pt           # YOLOv8m trained model
│   ├── uploads/              # Processed images directory
│   ├── batch_upload.py       # CLI tool for batch uploads
│   ├── batch_upload.bat      # Windows batch upload script
│   └── test_api.py           # API testing script
│
├── frontend/
│   ├── index.html            # Web interface
│   ├── script.js             # Frontend logic (with chunked upload)
│   └── style.css             # Styling
│
└── Documentation/
    └── BATCH_UPLOAD_FIX.md   # Batch upload guide
```

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/safety-equipment-detection.git
   cd Hackthon
   ```

2. **Install Python dependencies**
   ```bash
   cd Backend
   pip install -r requirements.txt
   ```

3. **Place the model**
   - Ensure `best.pt` is in the `Backend/models/` directory
   - Download from your training output if needed

## Quick Start

### Option 1: Web Interface (Easiest)

1. **Start the backend**
   ```bash
   cd Backend
   python app.py
   ```

2. **Open the frontend**
   ```bash
   # Open in your browser:
   file:///path/to/frontend/index.html
   ```

3. **Upload images**
   - Single image: Use "Single Detection" tab
   - Batch (1000+): Use "Batch Detection" tab
   - The frontend automatically chunks uploads (default 50 per request)

### Option 2: CLI Tool

For processing a folder of images:

```bash
cd Backend

# Simple usage
python batch_upload.py C:\path\to\images

# With custom chunk size
python batch_upload.py C:\path\to\images 50 0.25

# Parameters:
# - image_directory: Path to folder with images
# - chunk_size: Images per request (default 50, max 100)
# - confidence: Detection threshold 0-1 (default 0.25)
```

### Option 3: REST API

```python
import requests

# Single image prediction
with open('image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/predict/single', files=files)
    print(response.json())

# Batch prediction (chunked automatically by frontend)
files = [('files', open(f, 'rb')) for f in image_list[:50]]
response = requests.post('http://localhost:8000/predict/batch-chunked', files=files)
print(response.json())
```

## API Endpoints

### Health Check
```
GET /health
Response: {"status": "healthy", "model_loaded": true}
```

### Model Info
```
GET /model-info
Response: {
  "model": "YOLOv8m Fine-tuned",
  "classes": 7,
  "mAP": 84.1,
  "classes_list": {...}
}
```

### Single Image Prediction
```
POST /predict/single
Parameters: file (image), confidence (0-1)
Response: {"detections_count": 3, "detections": [...], ...}
```

### Batch Prediction (Chunked)
```
POST /predict/batch-chunked
Parameters: files (list), confidence (0-1), chunk_size (int)
Response: {"total_images": 50, "total_detections": 234, ...}
```

## Performance

- **Processing Speed**: ~370ms per image
- **Batch Processing (50 images)**: ~20-30 seconds per chunk
- **1400 Images**: ~6-14 minutes total (depends on hardware)

## Handling Large Batches

For 1000+ images:

1. **Automatic Chunking** (Frontend)
   - The web interface automatically chunks files (default 50)
   - No additional configuration needed

2. **CLI Chunking** (CLI Tool)
   ```bash
   # Safe for 1400 images
   python batch_upload.py <images> 50
   ```

3. **Chunk Size Recommendations**
   - 50 images/request: ✅ Most stable
   - 100 images/request: ✅ Faster, still safe
   - >100 images/request: ⚠️ Not recommended

## Troubleshooting

### Backend won't start
```bash
# Ensure Python and dependencies are installed
pip install -r requirements.txt

# If port 8000 is busy, use:
python -m uvicorn app:app --port 8001
```

### Images not processing
- Check that images are valid (JPG, PNG, BMP, TIFF)
- Verify model file exists: `Backend/models/best.pt`
- Check backend logs for detailed errors

### Too many files error
- Reduce chunk size: `python batch_upload.py <path> 50`
- Check that total files < 1000 per request

## Results

After processing, results are saved in:
- **Annotated images**: `Backend/uploads/annotated_*.jpg`
- **Batch summary**: `Backend/batch_results.json`

## Technologies

- **Backend**: FastAPI, Uvicorn, PyTorch
- **ML Model**: YOLOv8m (Ultralytics)
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Image Processing**: OpenCV, Pillow

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions:
1. Check the [Batch Upload Guide](BATCH_UPLOAD_FIX.md)
2. Review API logs in the backend terminal
3. Test with `Backend/test_api.py`

## Contributors

Hafiz - Initial development

---

**Happy Detecting! 🎯**
