from pydantic import BaseModel, Field
from typing import Dict

class PredictionResponse(BaseModel):
    predicted_category: float = Field(..., description="The predicted insurance premium amount.", example='High')
    confidence: float = Field(..., description="The confidence score of the prediction.", example=0.85)
    probabilities: Dict[str, float] = Field(..., description="Probabilities for each insurance premium category.", example={"Low": 0.1, "Medium": 0.3, "High": 0.6})