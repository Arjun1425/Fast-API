from fastapi import FastAPI, HTTPException, Query
from starlette.responses import JSONResponse   
import json
from pydantic import BaseModel, Field, computed_field
from typing import Optional, Annotated, Literal

class Patient(BaseModel):
    id: Annotated[str, Field(description = "Id of the Patient.", examples = ["P001", "P002"])]
    name: Annotated[str, Field(description = "Enter the name of the patient")]
    age: Annotated[int, Field(gt = 0, description = "Enter the age of the patient")]
    city: Annotated[str, Field(description = "Enter the city where the person lives.")]
    gender: Annotated[Literal['male', 'female', 'others'], Field(description = "Enter the gender of the person male, female or others.")]
    height: Annotated[float, Field(gt = 0, description = "Enter the height in meters.")]
    weight: Annotated[float, Field(gt = 0, description = "Enter the weight in Kg.")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight/self.height**2, 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        
        bmi_value = self.bmi
        if bmi_value < 18.5:
            return "Underweight"
        elif bmi_value < 30:
            return "Normal"
        else:
            return "Obese"   


class PatientUpdate(BaseModel):
    
    name: Annotated[Optional[str], Field(description = "Enter the name of the patient")]
    age: Annotated[Optional[int], Field(gt = 0, description = "Enter the age of the patient")]
    city: Annotated[Optional[str], Field(description = "Enter the city where the person lives.")]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(description = "Enter the gender of the person male, female or others.")]
    height: Annotated[Optional[float], Field(gt = 0, description = "Enter the height in meters.")]
    weight: Annotated[Optional[float], Field(gt = 0, description = "Enter the weight in Kg.")]


app = FastAPI()

def load_data():
    with open("patients.json", 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("patients.json", 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {"message": "Patient Management System"}

@app.get("/about")
def about():
    return {"message": "A fullly functional patient management system built with FastAPI."}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str):
    data = load_data()
    patient_ = data.get(patient_id)
    if patient_ is not None:
        return patient_
    else: 
        raise HTTPException(status_code = 404, detail = "Patient data is not available. Please add the right name.")
    
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description = "Sort the query based on height, bmi, and, weight."), order_by: str = Query("asc", description = "You want to sort in asc or des order")):
    data = load_data()
    validate_sort_by = ["height", "weight", "bmi"]
    if sort_by not in validate_sort_by:
        raise HTTPException(status_code = 400, detail = f"Please choose from {validate_sort_by}")
    if order_by not in ['asc', 'desc']:
        raise HTTPException(status_code = 400, detail = f"Please choose from 'asc' or 'desc'")
    
    sorted_data = sorted(data.values(), key = lambda x: x[sort_by], reverse = (order_by == "desc"))
    return sorted_data


@app.post("/create")
def create_patient(patient: Patient):

    #load existing data
    data = load_data()
    
    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code = 400, detail = "Patient already exist.")

    # Update the new patient database
    data[patient.id] = patient.model_dump(exclude = ["id"])

    save_data(data)

    return JSONResponse(status_code = 201, content = {"message": "Patient data created successfully."})

@app.put("/edit")
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code = 400, detail = "Patient is not present in the data.")
    
    existing_patient = data[patient_id]

    # convert patient_update in dictionary
    new_patient_data = patient_update.model_dump(exclude_unset = True)

    for key, value in new_patient_data.items():
        existing_patient[key] = value

    # Now if weight is changing then bmi will also change so what can we do here is convert existing_patient --> Pydantic_object patient (it will calculate the bmi, and verdict) --> conver again in dictionary
    existing_patient["id"] = patient_id        # To add the patient id.
    existing_patient = Patient(**existing_patient)
    existing_patient = existing_patient.model_dump(exclude = ["id"])

    data[patient_id] = existing_patient
    save_data(data)

    return JSONResponse(status_code = 201, content = {'message': 'Patient details has been updated'})

@app.delete("/delete/{patient_id}")
def delete(patient_id: str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code = 400, detail= "Patient is not present in the data. Enter the correct id.")
    
    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code = 200, content = {"message": "Patient data has been deleted successfully."})