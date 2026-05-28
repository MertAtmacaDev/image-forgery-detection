import os
from fastapi import APIRouter, HTTPException
from schemas import AiModelResult
from services.ai_detection import predict_cnn, predict_cnn_lstm

router = APIRouter()

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../uploads"))

@router.post("/ai-analyze/{filename}", response_model=dict[str, AiModelResult])
async def ai_analyze_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404, 
            detail=f"Target image file not found at path: {file_path}"
        )
    
    try:
        cnn_result = predict_cnn(file_path)
        if "error" in cnn_result:
            raise Exception(cnn_result["error"])
            
        cnn_lstm_result = predict_cnn_lstm(file_path)
        if "error" in cnn_lstm_result:
            raise Exception(cnn_lstm_result["error"])
            
        return {
            "resnet18_prediction": cnn_result,
            "cnn_lstm_prediction": cnn_lstm_result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"AI Inference Pipeline Failure: {str(e)}"
        )