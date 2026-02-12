# FastAPI & ML Projects

A collection of machine learning projects served through FastAPI and Streamlit, demonstrating end-to-end ML workflows — from data preprocessing and model training to API deployment and interactive frontends.

---

## Projects

### 1. Patient Management System (FastAPI CRUD API)

A RESTful API built with FastAPI for managing patient health records. Supports full CRUD operations with automatic BMI calculation and health verdict classification.

**Tech Stack:** FastAPI, Pydantic, Uvicorn

**Features:**
- Create, read, update, and delete patient records
- Automatic BMI computation and health verdict (Underweight / Normal / Obese) using Pydantic computed fields
- Sort patients by height, weight, or BMI in ascending/descending order
- Input validation with type hints and annotated constraints
- JSON file-based persistence

**API Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/about` | About the system |
| GET | `/view` | View all patients |
| GET | `/patient/{patient_id}` | View a specific patient |
| GET | `/sort?sort_by=&order_by=` | Sort patients by height, weight, or BMI |
| POST | `/create` | Add a new patient |
| PUT | `/edit?patient_id=` | Update patient details |
| DELETE | `/delete/{patient_id}` | Delete a patient record |

**Run it:**
```bash
uvicorn main:app --reload
```

---

### 2. Insurance Premium Prediction API

A machine learning-powered API that predicts insurance premium categories (Low / Medium / High) based on user demographics, health, and lifestyle data. Includes a Streamlit frontend for interactive predictions.

**Tech Stack:** FastAPI, scikit-learn (Random Forest Classifier), Pandas, Pydantic, Streamlit, Docker

**ML Pipeline:**
- **Model:** Random Forest Classifier with scikit-learn Pipeline (OneHotEncoder + RandomForestClassifier)
- **Engineered Features:** BMI (from height/weight), age group binning, lifestyle risk score (smoking + BMI), city tier classification (Tier 1/2/3 Indian cities)
- **Accuracy:** 90% on test set
- **Output:** Predicted category, confidence score, and per-class probabilities

**Project Structure:**
```
Insurance_premium_project/
├── app.py                  # FastAPI application with /predict and /health endpoints
├── schema/
│   ├── user_input.py       # Pydantic model with computed fields (BMI, lifestyle risk, age group, city tier)
│   └── prediction_response.py  # Response schema
├── model/
│   ├── predict.py          # Prediction logic using pickled model
│   └── model.pkl           # Trained Random Forest model
├── config/
│   └── city_tier.py        # Tier 1 and Tier 2 Indian city lists
├── Dockerfile              # Docker containerization (Python 3.11-slim)
├── requirements.txt        # Conda environment spec
└── requirements_pip.txt    # Pip requirements
```

**API Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check with model version |
| POST | `/predict` | Predict insurance premium category |

**Sample Request Body (`/predict`):**
```json
{
  "age": 30,
  "height": 1.75,
  "weight": 70.0,
  "city": "Mumbai",
  "income_lpa": 12,
  "smoker": false,
  "occupation": "private_job"
}
```

> The API automatically computes derived features from the raw input: **BMI**, **age group**, **lifestyle risk score**, and **city tier** — these are passed to the model internally via Pydantic computed fields.

**Run it:**
```bash
# API
cd Insurance_premium_project
uvicorn app:app --reload

# Frontend (from root directory)
streamlit run frontend.py
```

**Docker:**
```bash
cd Insurance_premium_project
docker build -t insurance-api .
docker run -p 8000:8000 insurance-api
```

---

### 3. Laptop Price Predictor (Streamlit App)

An interactive Streamlit web application that predicts laptop prices based on hardware specifications using a pre-trained regression model.

**Tech Stack:** Streamlit, scikit-learn, NumPy, Pandas, Docker

**Features:**
- Predicts laptop price from 12 input features: brand, type, RAM, weight, touchscreen, IPS display, screen size, resolution (PPI), CPU, HDD, SSD, GPU, and OS
- Uses a pre-trained scikit-learn pipeline (`pipe.pkl`) with log-transformed price prediction
- Heroku-ready with Procfile and setup script

**Run it:**
```bash
cd laptop-price-predictor-regression-project
streamlit run app.py
```

**Docker:**
```bash
cd laptop-price-predictor-regression-project
docker build -t laptop-predictor .
docker run -p 8501:8501 laptop-predictor
```

---

### 4. Jupyter Notebooks

- **`fastapi_ml_model.ipynb`** — Full ML workflow for the insurance premium model: data exploration, feature engineering (BMI, age groups, lifestyle risk, city tiers), pipeline construction (ColumnTransformer + RandomForestClassifier), train/test split, evaluation (90% accuracy), and model serialization with pickle.
- **`pydantic.ipynb`** — Quick reference demonstrating Pydantic's `Field` and `Annotated` type patterns for input validation.

---

## Tech Stack Overview

| Category | Technologies |
|----------|-------------|
| API Framework | FastAPI, Uvicorn, Starlette |
| ML / Data | scikit-learn, Pandas, NumPy |
| Validation | Pydantic (computed fields, field validators, annotated types) |
| Frontend | Streamlit |
| Containerization | Docker |
| Deployment | Heroku (Procfile), Docker |
| Language | Python 3.7+ / 3.11 |

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/yourusername/FastAPI.git
cd FastAPI

# Install dependencies
pip install fastapi uvicorn scikit-learn pandas numpy streamlit pydantic

# Run the Patient Management API
uvicorn main:app --reload

# Run the Insurance Premium API
cd Insurance_premium_project && uvicorn app:app --reload

# Run the Laptop Price Predictor
cd laptop-price-predictor-regression-project && streamlit run app.py
```

---

## Author

**Arjun**

Built to demonstrate end-to-end machine learning deployment using FastAPI, Streamlit, and Docker.
