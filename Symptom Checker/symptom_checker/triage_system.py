# symptom_checker/triage_system.py
from .data_loader import MedicalDataLoader
from .disease_predictor import DiseasePredictor
from .rag_precaution_fetcher import RAGPrecautionFetcher
from .symptom_validator import SymptomValidator
from .risk_assessment import RiskAssessor
from .severity_assessment import SeverityAssessor
from .care_recommendation import CareRecommender

class TriageSystem:
    def __init__(self, data_path='data/', serp_api_key=None, groq_api_key=None):
        # 1. Load and process all data
        data_loader = MedicalDataLoader(data_path)
        data_loader.load_and_process_data()
        self.processed_data = data_loader.get_processed_data()

        # Extract data for easy access
        self.all_symptoms = self.processed_data['all_symptoms']
        self.severity_mapping = self.processed_data['severity_mapping']
        self.description_mapping = self.processed_data['description_mapping']
        self.precaution_mapping = self.processed_data['precaution_mapping']

        # 2. Initialize and train the disease predictor
        self.predictor = DiseasePredictor()
        self.predictor.train(self.processed_data['X_train'], self.processed_data['y_train'])
        
        # 3. Initialize the RAG fetcher for dynamic information
        self.rag_fetcher = RAGPrecautionFetcher(serp_api_key, groq_api_key)
        
        # ## New Method for logging status ##
        self._log_status()

    def _log_status(self):
        """Logs the status of the system after initialization."""
        print("✅ Triage System Initialized Successfully.")
        print(f"-> Loaded {len(self.all_symptoms)} symptoms.")
        print("-> Disease prediction model trained.")


    def assess_patient(self, patient_symptoms):
        """
        Runs the full triage assessment for a given list of patient symptoms.
        """
        print(f"\nAssessing symptoms: {patient_symptoms}")

        # Step 1: Validate symptoms against our known list
        validated_symptoms = SymptomValidator.validate(patient_symptoms, self.all_symptoms)
        if not validated_symptoms:
            return {"error": "No valid symptoms provided or recognized."}

        # Step 2: Calculate risk score
        risk_score = RiskAssessor.calculate(validated_symptoms, self.severity_mapping)

        # Step 3: Assess severity level
        severity_level = SeverityAssessor.classify(risk_score)

        # Step 4: Recommend care
        care_recommendation = CareRecommender.recommend(severity_level)

        # Step 5: Predict the most likely disease
        predicted_disease = self.predictor.predict(validated_symptoms)
        
        # Step 6: Fetch information about the predicted disease
        description = self.description_mapping.get(predicted_disease, "No description available.")
        
        try:
            print(f"Fetching RAG precautions for: {predicted_disease}")
            precautions = self.rag_fetcher.fetch_precautions(predicted_disease)
        except Exception as e:
            print(f"⚠️ RAG fetcher failed ({e}), falling back to local data.")
            precautions = self.precaution_mapping.get(predicted_disease, ["No specific precautions found."])

        return {
            "validated_symptoms": validated_symptoms,
            "risk_score": risk_score,
            "severity_level": severity_level,
            "care_recommendation": care_recommendation,
            "predicted_disease": {
                "name": predicted_disease.title(),
                "description": description,
                "precautions": precautions
            }
        }
