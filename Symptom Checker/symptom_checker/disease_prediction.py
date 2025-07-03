from symptom_checker.disease_predictor import DiseasePredictor

def predict_disease(symptoms, symptom_disease_map):
    return DiseasePredictor.predict(symptoms, symptom_disease_map)
