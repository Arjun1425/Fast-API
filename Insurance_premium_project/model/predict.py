import pandas as pd
import pickle

# import the ml model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

MODEL_VERSION = "1.0.0"

# Get class from the model
class_labels = model.classes_.tolist()

def predict_output(user_input: dict) -> float: 
    input_df = pd.DataFrame([user_input])
    predicted_class = model.predict(input_df)[0]
    
    # Get the probability of all classes
    predicted_proba = model.predict_proba(input_df)[0]
    confidence_score = max(predicted_proba)

    # create mapping of class to probability
    class_proba_mapping = {class_labels[i]: predicted_proba[i] for i in range(len(class_labels))}

    return {
        "predicted_class": predicted_class,
        "confidence_score": confidence_score,
        "class_probabilities": class_proba_mapping
        }