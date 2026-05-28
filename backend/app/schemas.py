from pydantic import BaseModel

class AlgorithmResult(BaseModel):
    keypoint_count: int
    match_count: int
    is_forged: bool
    result_image_base64: str

class AiModelResult(BaseModel):
    model: str
    prediction: str
    confidence: float