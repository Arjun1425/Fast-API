from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse   
import json
from schema.prediction_response import PredictionResponse
from schema.user_input import model_input
from model.predict import predict_output, MODEL_VERSION

app = FastAPI()

@app.get('/')
def home():
    return JSONResponse(status_code = 200, content = {"message": "Welcome to Insurance Premium Prediction API. Use the /predict endpoint to get predictions."})

@app.get('/health')
def health():
    return JSONResponse(status_code = 200, content = {"status": "healthy", "model_version": MODEL_VERSION})

@app.post('/predict', response_model=PredictionResponse)
def predict(user_input: model_input):
    
    # Convert input data into pandas df from pydantic.
    input_user = {
        'age_group': user_input.age_group,
        'bmi': user_input.bmi,
        'lifestyle_risk': user_input.lifestyle_risk,
        'city_tier': user_input.city_tier,
        'income_lpa': user_input.income_lpa,
        'occupation': user_input.occupation
    }

    try: 
        prediction = predict_output(input_user)
        return JSONResponse(status_code = 200, content = {"Response": prediction})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {str(e)}")