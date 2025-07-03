from symptom_checker.triage_system import TriageSystem
import os
from dotenv import load_dotenv

# Load environment variables (SERP API key)
load_dotenv(dotenv_path='C:/Users/akshi/OneDrive/Documents/Symptom Checker/symptom_checker/safe.env')
SERP_API_KEY = os.getenv("SERP_API_KEY")

def main():
    triage = TriageSystem(data_path="data/", serp_api_key=SERP_API_KEY)

    # Example symptoms (you can modify this or accept user input)
    patient_symptoms = ['fever', 'cough', 'shortness of breath']

    result = triage.assess_patient(patient_symptoms)

    # Display result
    print("\n📋 Triage Summary")
    print(f"✅ Validated Symptoms: {result['validated_symptoms']}")
    print(f"\n💥 Risk Score: {result['risk_score']}")
    print(f"\n⚠️ Severity Level: {result['severity_level']}")
    print(f"\n💡 Care Recommendation: {result['care_recommendation']}\n")

    print("🩺 Predicted Diseases and Details:")
    for detail in result['disease_details']:
        print(f"  ➡ Disease: {detail['disease']}")
        print(f"     Description: {detail['description']}")
        print(f"     Precautions: {detail['precautions']}\n")

if __name__ == "__main__":
    main()
