"""
API Testing Script - Test all endpoints without using the frontend
Run this after starting the backend with: python app.py
"""

import requests
import json
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000"
TEST_IMAGE_PATH = None  # Set this to your test image path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")

def test_connection():
    """Test if backend is running"""
    print("\n" + "="*50)
    print("1. Testing API Connection")
    print("="*50)
    
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            print_success("Backend is running!")
            print_info(f"Response: {response.json()}")
            return True
        else:
            print_error(f"Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend at http://localhost:8000")
        print_warning("Make sure to run: python app.py in Backend folder")
        return False
    except Exception as e:
        print_error(f"Connection error: {str(e)}")
        return False

def test_health():
    """Test health endpoint"""
    print("\n" + "="*50)
    print("2. Testing Health Endpoint")
    print("="*50)
    
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_success("Health check passed!")
            print_info(f"Status: {data.get('status')}")
            print_info(f"Model loaded: {data.get('model_loaded')}")
            return True
        else:
            print_error(f"Health check failed with status: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {str(e)}")
        return False

def test_model_info():
    """Test model info endpoint"""
    print("\n" + "="*50)
    print("3. Testing Model Info Endpoint")
    print("="*50)
    
    try:
        response = requests.get(f"{API_BASE_URL}/model-info")
        if response.status_code == 200:
            data = response.json()
            print_success("Model info retrieved!")
            print_info(f"Model: {data.get('model')}")
            print_info(f"Classes: {data.get('classes')}")
            print_info(f"mAP: {data.get('mAP')}")
            print_info(f"Classes list: {list(data.get('classes_list', {}).values())}")
            return True
        else:
            print_error(f"Failed with status: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_single_prediction(image_path):
    """Test single image prediction"""
    print("\n" + "="*50)
    print("4. Testing Single Image Prediction")
    print("="*50)
    
    if not image_path or not Path(image_path).exists():
        print_warning("Skipping single prediction test - no image provided")
        print_info("To test: provide image path when running this script")
        return None
    
    try:
        print_info(f"Testing with image: {image_path}")
        
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {'confidence': 0.25}
            response = requests.post(
                f"{API_BASE_URL}/predict/single",
                files=files,
                data=data
            )
        
        if response.status_code == 200:
            result = response.json()
            print_success("Single prediction successful!")
            print_info(f"Detections found: {result.get('detections_count')}")
            print_info(f"Filename: {result.get('filename')}")
            print_info(f"Confidence threshold: {result.get('confidence_threshold')}")
            if result.get('detections'):
                print_info("Detected objects:")
                for det in result.get('detections', []):
                    print(f"  - {det['class']}: {det['confidence']*100:.1f}%")
            return True
        else:
            print_error(f"Prediction failed with status: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Prediction error: {str(e)}")
        return False

def test_batch_prediction(image_paths):
    """Test batch image prediction"""
    print("\n" + "="*50)
    print("5. Testing Batch Prediction")
    print("="*50)
    
    if not image_paths or all(not Path(p).exists() for p in image_paths):
        print_warning("Skipping batch prediction test - no images provided")
        return None
    
    valid_images = [p for p in image_paths if Path(p).exists()]
    
    if not valid_images:
        print_warning("No valid images found for batch test")
        return None
    
    try:
        print_info(f"Testing with {len(valid_images)} image(s)")
        
        files = [('files', open(p, 'rb')) for p in valid_images]
        data = {'confidence': 0.25}
        response = requests.post(
            f"{API_BASE_URL}/predict/batch",
            files=files,
            data=data
        )
        
        # Close all files
        for _, f in files:
            f.close()
        
        if response.status_code == 200:
            result = response.json()
            print_success("Batch prediction successful!")
            print_info(f"Total images: {result.get('total_images')}")
            print_info(f"Total detections: {result.get('total_detections')}")
            print_info(f"Avg detections per image: {result.get('avg_detections_per_image')}")
            return True
        else:
            print_error(f"Batch prediction failed with status: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Batch prediction error: {str(e)}")
        return False

def main():
    print(f"\n{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║   Safety Equipment Detection API - Test Suite          ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(Colors.END)
    
    print_info(f"API URL: {API_BASE_URL}")
    
    # Run tests
    if not test_connection():
        print_error("Cannot proceed - backend not running")
        return
    
    test_health()
    test_model_info()
    test_single_prediction(TEST_IMAGE_PATH)
    test_batch_prediction([TEST_IMAGE_PATH] if TEST_IMAGE_PATH else [])
    
    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)
    print_success("All available tests completed!")
    print_info("To test with images, set TEST_IMAGE_PATH in this script")
    print_info("Or use the web interface: open frontend/index.html")

if __name__ == "__main__":
    main()
