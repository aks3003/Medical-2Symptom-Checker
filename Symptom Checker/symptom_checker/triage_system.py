import pandas as pd
from symptom_checker.disease_predictor import DiseasePredictor
from symptom_checker.rag_precaution_fetcher import RAGPrecautionFetcher
from symptom_checker.data_loader import MedicalDataLoader

class TriageSystem:
    def __init__(self, data_path, serp_api_key):
        self.data_path = data_path
        self.data_loader = MedicalDataLoader(data_path)
        self.data_loader.load_datasets()

        self.symptom_disease_map = self.data_loader.processed_data['symptom_disease_map']
        self.all_symptoms = self.data_loader.processed_data['all_symptoms']
        self.severity_mapping = self.data_loader.processed_data['severity_mapping']

        self.rag_fetcher = RAGPrecautionFetcher(serp_api_key)

    def assess_patient(self, patient_symptoms):
        print(f"\n🔍 Assessing patient with symptoms: {patient_symptoms}")

        validated_symptoms = self.validate_symptoms(patient_symptoms)
        risk_score = self.calculate_risk_score(validated_symptoms)
        severity_level = self.determine_severity_level(risk_score)
        care_recommendation = self.recommend_care(severity_level)

        predicted_diseases = DiseasePredictor.predict(validated_symptoms, self.symptom_disease_map)

        disease_details = []
        for disease in predicted_diseases:
            description = self.rag_fetcher.fetch_condition(validated_symptoms)
            precautions_text = self.rag_fetcher.fetch_precautions(disease)

            disease_details.append({
                "disease": disease,
                "description": description,
                "precautions": precautions_text
            })

        return {
            "validated_symptoms": validated_symptoms,
            "risk_score": risk_score,
            "severity_level": severity_level,
            "care_recommendation": care_recommendation,
            "disease_details": disease_details
        }

    def validate_symptoms(self, symptoms):
        validated = []
        for symptom in symptoms:
            norm_symptom = symptom.strip().lower().replace(' ', '_')
            if norm_symptom in self.all_symptoms:
                validated.append(norm_symptom)
        return validated

    def calculate_risk_score(self, validated_symptoms):
        # Use dataset severity mapping instead of hardcoding
        return sum(self.severity_mapping.get(symptom, 1) for symptom in validated_symptoms)

    def determine_severity_level(self, risk_score):
        if risk_score >= 12:
            return "HIGH"
        elif risk_score >= 8:
            return "MEDIUM"
        else:
            return "LOW"

    def recommend_care(self, severity_level):
        if severity_level == "HIGH":
            return "IMMEDIATE MEDICAL ATTENTION"
        elif severity_level == "MEDIUM":
            return "CONSULT DOCTOR"
        else:
            return "SELF CARE"
