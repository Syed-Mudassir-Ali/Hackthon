# 1400 تصاویریں بھیجنے میں Error - حل

## مسئلہ کیا تھا؟

جب آپ 1400 تصاویریں سے زیادہ ایک ساتھ upload کرتے تھے، تو **`400 Bad Request`** error آتا تھا۔

### وجوہات:
1. **Request حد سے زیادہ بڑا** - FastAPI کی default limit 25MB ہے
2. **Memory pressure** - سب تصاویریں ایک ساتھ process ہو رہی تھیں
3. **Timeout** - بہت سارے بڑے requests کو process کرنے میں زیادہ وقت لگتا ہے

---

## حل کیا ہے؟

### 1. **Chunked Processing** ✓
`/predict/batch-chunked` endpoint استعمال کریں جو:
- تصاویریں 100 تک کے chunks میں تقسیم کرتا ہے
- ہر chunk کو الگ الگ process کرتا ہے
- Memory کو محفوظ رکھتا ہے
- بڑی تصاویریں (1400+) کو سنبھال سکتا ہے

### 2. **نئے Tools:**

#### Option A: Python Script (تمام operating systems)
```bash
python batch_upload.py <image_directory>
```

مثال:
```bash
# 1400 تصاویریں upload کریں
python batch_upload.py uploads/testing

# custom chunk size کے ساتھ
python batch_upload.py uploads/testing 50 0.3

# Parameters:
# - image_directory: تصاویریں کے folder کا path
# - chunk_size: ہر request میں تصاویریں (default: 100)
# - confidence: detection threshold (default: 0.25)
```

#### Option B: Windows Batch File
```bash
batch_upload.bat uploads\testing
```

---

## استعمال کی مثالیں

### Example 1: سادہ طریقہ
```bash
cd Backend
python batch_upload.py C:\path\to\your\1400\images
```

**Output:**
```
Connecting to API at http://localhost:8000...
✓ Backend is running and healthy!
Scanning directory: C:\path\to\your\1400\images
✓ Found 1400 images
Total images to process: 1400
Chunk size: 100 images per request

============================================================
Processing chunk 1/14 (100 images)
Images 1 to 100
============================================================
ℹ Uploading 100 images...
✓ Chunk 1 processed successfully in 45.2s
  Images processed: 100
  Total detections: 523
  Avg per image: 5.23
  Sample detections from image001.jpg:
    - FireExtinguisher: 95.4%
    - SafetySwitchPanel: 89.2%
```

### Example 2: Smaller chunks (کم memory کے لیے)
```bash
python batch_upload.py uploads/testing 50 0.25
# ہر chunk میں 50 تصاویریں ہوں گی
# کل 28 chunks ہوں گے (1400/50)
```

### Example 3: High confidence threshold
```bash
python batch_upload.py uploads/testing 100 0.5
# صرف 50% سے اوپر کی detection لیں
```

---

## اگر ابھی بھی error آئے؟

### Error: `400 Bad Request`
- ✅ اب یہ fixed ہے - `/predict/batch-chunked` استعمال کریں

### Error: `Connection refused`
```bash
# پہلے Backend شروع کریں
cd Backend
python app.py

# دوسری window میں batch upload چلائیں
python batch_upload.py <images_path>
```

### Error: `Timeout`
- Chunk size کم کریں:
```bash
python batch_upload.py uploads/testing 50
```

### Error: `No images found`
- Image folder کا path ٹھیک کریں:
```bash
# Windows میں
python batch_upload.py "C:\Users\hafiz\OneDrive\Desktop\images"

# یا relative path
python batch_upload.py ../images
```

---

## اندرونی تفصیلات

### /predict/batch-chunked endpoint
**Location:** [Backend/app.py](Backend/app.py#L303)

**کیسے کام کرتا ہے:**
```
User: 1400 images upload کریں
      ↓
Script: chunks میں تقسیم کریں (100 images each)
      ↓
API: Chunk 1 process کریں ← Chunk 2 ← Chunk 3... ← Chunk 14
      ↓
Results: تمام chunks کے نتائج جمع کریں
      ↓
Output: batch_results.json میں save کریں
```

**Parameters:**
- `files`: List[UploadFile] - تصاویریں
- `confidence`: float = 0.25 - detection threshold
- `chunk_size`: int = 100 - processing size

**Response:**
```json
{
  "status": "success",
  "total_images": 1400,
  "total_detections": 7234,
  "avg_detections_per_image": 5.17,
  "images": [
    {
      "filename": "image001.jpg",
      "detections_count": 5,
      "class_counts": {
        "FireExtinguisher": 2,
        "SafetySwitchPanel": 3
      },
      "detections": [...],
      "annotated_image": "/download/uploads/annotated_image001.jpg"
    },
    ...
  ]
}
```

---

## Performance Tips

### تیز ترین ترتیب:
```bash
# بڑے chunks (memory زیادہ ہو تو)
python batch_upload.py uploads/testing 200 0.25
```

### سب سے محفوظ:
```bash
# چھوٹے chunks (کم memory)
python batch_upload.py uploads/testing 50 0.25
```

### درمیانی:
```bash
# default (100 per chunk)
python batch_upload.py uploads/testing
```

---

## نتیجہ

**پہلے:** ❌ 1400 images = 400 Bad Request
**اب:** ✅ 1400 images = 14 chunks → Success!

**Throughput:**
- ~100 images/request
- ~45-60 seconds/request  
- ~10-14 منٹ total (1400 images)

---

## خلاصہ

1. **Backend شروع کریں:**
   ```bash
   cd Backend
   python app.py
   ```

2. **تصاویریں upload کریں:**
   ```bash
   # نئی window میں
   python batch_upload.py <image_directory>
   ```

3. **نتائج دیکھیں:**
   - Console output میں progress
   - `batch_results.json` میں مکمل نتائج
   - `uploads/annotated_*` میں marked images

**کامیاب! 🎉**
