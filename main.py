from fastapi import FastAPI, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open("patients.json", 'r') as f:
        data = json.load(f)
    return data

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
    if order_by not in ['asc', 'dsc']:
        raise HTTPException(status_code = 400, detail = f"Please choose from 'asc' or 'dsc'")
    
    sorted_data = sorted(data.values(), key = lambda x: x[sort_by], reverse = (order_by == "dsc"))
    return sorted_data
