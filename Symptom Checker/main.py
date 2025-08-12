# main.py
import os
from dotenv import load_dotenv
from symptom_checker.triage_system import TriageSystem
import pprint

def main():
    """
    Main function to initialize and run the symptom checker.
    """
    # Load environment variables from .env file
    # Ensure you have a 'safe.env' file with your SERP_API_KEY and GROQ_API_KEY
    load_dotenv(dotenv_path='safe.env')
    
    serp_api_key = os.getenv("SERP_API_KEY")
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not serp_api_key or not groq_api_key:
        print("❌ API Keys are missing! Please create a 'safe.env' file with SERP_API_KEY and GROQ_API_KEY.")
        return

    # Initialize the Triage System (this will load data and train the model)
    try:
        triage_system = TriageSystem(
            serp_api_key=serp_api_key,
            groq_api_key=groq_api_key
        )
    except Exception as e:
        print(f"❌ Failed to initialize the Triage System: {e}")
        return

    # --- Example Patient Assessment ---
    # You can change these symptoms to test different scenarios
    patient_symptoms = ["itching", "skin rash", "nodal skin eruptions"] # Example for Fungal infection
    # patient_symptoms = ["continuous sneezing", "shivering", "chills"] # Example for Allergy
    # patient_symptoms = ["acidity", "indigestion", "headache", "blurred_and_distorted_vision"] # Example for Migraine
    
    # Get the assessment result
    result = triage_system.assess_patient(patient_symptoms)

    # Pretty print the final result
    print("\n\n--- Final Assessment Report ---")
    pprint.pprint(result)
    print("-----------------------------\n")


if __name__ == "__main__":
    main()
