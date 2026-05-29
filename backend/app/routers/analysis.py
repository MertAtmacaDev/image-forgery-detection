import os
import base64
import cv2
from fastapi import APIRouter, HTTPException

from services.classical_detection import detect_sift, detect_orb, detect_akaze, detect_brisk

from schemas import AlgorithmResult

router = APIRouter()

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../uploads"))

@router.post("/analyze/{filename}", response_model=dict[str, AlgorithmResult])
async def analyze_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404, 
            detail=f"image not found. path: {file_path}"
        )
    
    try:
        algorithms = {
            "SIFT": detect_sift,
            "ORB": detect_orb,
            "AKAZE": detect_akaze,
            "BRISK": detect_brisk
        }
        
        analysis_results = {}
        
        for name, detect_func in algorithms.items():
            res = detect_func(file_path)
            
            success, encoded_image = cv2.imencode('.jpg', res["result_image"])#image to base64
            if not success:
                raise Exception(f"{name} image does not encoding.")
            
            base64_str = base64.b64encode(encoded_image).decode('utf-8')
            full_base64_uri = f"data:image/jpeg;base64,{base64_str}"
            
            analysis_results[name] = {
                "keypoint_count": res["keypoint_count"],
                "match_count": res["match_count"],
                "is_forged": res["is_forged"],
                "result_image_base64": full_base64_uri
            }
            
        return analysis_results

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"server error: {str(e)}"
        )