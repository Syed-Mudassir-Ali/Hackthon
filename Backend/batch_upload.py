"""
Batch upload script for large image collections (1000+ images)
Splits images into chunks to avoid request size limits
"""

import requests
import json
import os
from pathlib import Path
import sys
from typing import List
import time

API_BASE_URL = "http://localhost:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.YELLOW}")

def print_progress(msg):
    print(f"{Colors.CYAN}{msg}{Colors.END}")

def get_image_files(directory: str) -> List[str]:
    """Get all image files from directory"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
    image_files = []
    
    path = Path(directory)
    if not path.exists():
        print_error(f"Directory not found: {directory}")
        return []
    
    for file in path.rglob('*'):
        if file.suffix.lower() in image_extensions:
            image_files.append(str(file))
    
    return sorted(image_files)

def upload_batch_chunked(
    image_files: List[str],
    confidence: float = 0.25,
    chunk_size: int = 50
) -> dict:
    """Upload images using chunked batch endpoint
    
    Note: FastAPI has a hard limit of 1000 form fields per request.
    Default chunk_size is 50 to stay safe. Max recommended is 100.
    """
    
    # Enforce maximum chunk size to avoid FastAPI limits
    if chunk_size > 100:
        print_warning(f"Chunk size reduced from {chunk_size} to 100 (FastAPI limit)")
        chunk_size = 100
    
    total_images = len(image_files)
    print_info(f"Total images to process: {total_images}")
    print_info(f"Chunk size: {chunk_size} images per request")
    
    all_results = {
        "total_images_processed": 0,
        "total_detections": 0,
        "chunks": []
    }
    
    num_chunks = (total_images + chunk_size - 1) // chunk_size
    
    for chunk_idx in range(num_chunks):
        start_idx = chunk_idx * chunk_size
        end_idx = min((chunk_idx + 1) * chunk_size, total_images)
        chunk_images = image_files[start_idx:end_idx]
        
        print_progress(f"\n{'='*60}")
        print_progress(f"Processing chunk {chunk_idx + 1}/{num_chunks} ({len(chunk_images)} images)")
        print_progress(f"Images {start_idx + 1} to {end_idx}")
        print_progress(f"{'='*60}")
        
        try:
            # Prepare files for upload
            files = []
            for img_path in chunk_images:
                if not Path(img_path).exists():
                    print_warning(f"File not found, skipping: {img_path}")
                    continue
                try:
                    files.append(('files', open(img_path, 'rb')))
                except Exception as e:
                    print_warning(f"Could not open file {img_path}: {e}")
                    continue
            
            if not files:
                print_warning(f"No valid files in chunk {chunk_idx + 1}")
                continue
            
            # Send request
            data = {
                'confidence': confidence,
                'chunk_size': chunk_size
            }
            
            print_info(f"Uploading {len(files)} images...")
            start_time = time.time()
            
            response = requests.post(
                f"{API_BASE_URL}/predict/batch-chunked",
                files=files,
                data=data,
                timeout=600  # 10 minute timeout
            )
            
            elapsed = time.time() - start_time
            
            # Close all files
            for _, f in files:
                f.close()
            
            if response.status_code == 200:
                result = response.json()
                print_success(f"Chunk {chunk_idx + 1} processed successfully in {elapsed:.1f}s")
                print_info(f"  Images processed: {result.get('total_images')}")
                print_info(f"  Total detections: {result.get('total_detections')}")
                print_info(f"  Avg per image: {result.get('avg_detections_per_image')}")
                
                all_results["total_images_processed"] += result.get('total_images', 0)
                all_results["total_detections"] += result.get('total_detections', 0)
                all_results["chunks"].append({
                    "chunk_number": chunk_idx + 1,
                    "images_processed": result.get('total_images'),
                    "detections": result.get('total_detections')
                })
                
                # Show sample detections
                if result.get('images') and len(result['images']) > 0:
                    first_image = result['images'][0]
                    if first_image.get('detections'):
                        print_info(f"  Sample detections from {first_image.get('filename')}:")
                        for det in first_image.get('detections', [])[:3]:
                            print(f"    - {det.get('class', 'Unknown')}: {det.get('confidence', 0)*100:.1f}%")
                
            else:
                print_error(f"Chunk {chunk_idx + 1} failed with status {response.status_code}")
                error_msg = response.text[:500]
                
                # Parse JSON error if possible
                try:
                    error_json = response.json()
                    if 'detail' in error_json:
                        error_msg = error_json['detail']
                except:
                    pass
                
                print_error(f"Response: {error_msg}")
                
                # Check if it's the "too many files" error
                if "Too many files" in error_msg or "1000" in error_msg:
                    print_warning("Reduce chunk_size and try again:")
                    print_warning("  python batch_upload.py <dir> 50")
                return None
            
            # Small delay between chunks
            if chunk_idx < num_chunks - 1:
                time.sleep(1)
                
        except requests.exceptions.Timeout:
            print_error(f"Chunk {chunk_idx + 1} timed out - try with smaller chunk_size")
            return None
        except Exception as e:
            print_error(f"Error processing chunk {chunk_idx + 1}: {str(e)}")
            return None
    
    # Final summary
    print_progress(f"\n{'='*60}")
    print_success("ALL CHUNKS PROCESSED SUCCESSFULLY!")
    print_progress(f"{'='*60}")
    print_info(f"Total images processed: {all_results['total_images_processed']}")
    print_info(f"Total detections found: {all_results['total_detections']}")
    print_info(f"Avg detections per image: {all_results['total_detections'] / max(all_results['total_images_processed'], 1):.2f}")
    
    return all_results

def main():
    print(f"\n{Colors.CYAN}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║   Batch Upload Script for Large Image Collections      ║")
    print("║   (Recommended for 1000+ images)                       ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(Colors.END)
    
    # Get directory from user
    if len(sys.argv) > 1:
        image_dir = sys.argv[1]
    else:
        print_info("Usage: python batch_upload.py <image_directory> [chunk_size] [confidence]")
        print_info("Example: python batch_upload.py ./my_images 50 0.25")
        print_info("")
        print_info("Chunk size recommendations:")
        print_info("  - 50 (default):  Safe for all systems")
        print_info("  - 100:          Safe, larger chunks")
        print_info("  - >100:        Not recommended (FastAPI limit is ~1000 form fields)")
        image_dir = input("\nEnter path to images directory: ").strip()
    
    if not image_dir:
        print_error("No directory specified")
        return
    
    # Get chunk size
    chunk_size = 50  # Changed default from 100 to 50
    if len(sys.argv) > 2:
        try:
            chunk_size = int(sys.argv[2])
            if chunk_size > 100:
                print_warning(f"Warning: Chunk size {chunk_size} is risky. Reducing to 100.")
                chunk_size = 100
        except ValueError:
            print_warning(f"Invalid chunk_size, using default: {chunk_size}")
    
    # Get confidence threshold
    confidence = 0.25
    if len(sys.argv) > 3:
        try:
            confidence = float(sys.argv[3])
        except ValueError:
            print_warning(f"Invalid confidence, using default: {confidence}")
    
    # Check backend
    print_info(f"Connecting to API at {API_BASE_URL}...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_success("Backend is running and healthy!")
        else:
            print_error("Backend is not responding properly")
            return
    except Exception as e:
        print_error(f"Cannot connect to backend: {e}")
        print_warning("Make sure to run: python app.py in the Backend directory")
        return
    
    # Get images
    print_info(f"Scanning directory: {image_dir}")
    image_files = get_image_files(image_dir)
    
    if not image_files:
        print_error("No image files found in directory")
        return
    
    print_success(f"Found {len(image_files)} images")
    
    # Upload
    result = upload_batch_chunked(image_files, confidence, chunk_size)
    
    if result:
        # Save results
        results_file = "batch_results.json"
        with open(results_file, 'w') as f:
            json.dump(result, f, indent=2)
        print_success(f"Results saved to {results_file}")

if __name__ == "__main__":
    main()
