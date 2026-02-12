from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Optional, Annotated, Literal
from config.city_tier import tier_1_cities, tier_2_cities

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
        
    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        return v.strip().title()
