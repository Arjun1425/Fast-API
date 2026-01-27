from turtle import pd
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse   
import json
from pydantic import BaseModel, Field, computed_field
from typing import Optional, Annotated, Literal
import pandas as pd
import pickle

# import the ml model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

class model_input(BaseModel):

    age: Annotated[int, Field(gt=0, description = "Enter the age of the person.")]
    height: Annotated[float, Field(gt=0, description = "Enter the height of the person in meters.")]
    weight: Annotated[float, Field(gt=0, description = "Enter the weight of the person in Kg.")]
    city: Annotated[str, Field(description = "Enter the city where you live.")]
    income_lpa: Annotated[int, Field(description = "Enter your income per year after tax.")]
    smoker: Annotated[bool, Field(description = "Enter True if you smoke otherwise False.")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the user')]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/self.height**2
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        
@app.post('/predict')
def predict(user_input: model_input):
    
    # Convert input data into pandas df from pydantic.
    input_df = pd.DataFrame([{
        'age_group': user_input.age_group,
        'bmi': user_input.bmi,
        'lifestyle_risk': user_input.lifestyle_risk,
        'city_tier': user_input.city_tier,
        'income_lpa': user_input.income_lpa,
        'occupation': user_input.occupation
    }])

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code = 200, content = {"Prediction": prediction})