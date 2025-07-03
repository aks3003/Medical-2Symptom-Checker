import streamlit as st
from symptom_checker.triage_system import TriageSystem
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()
SERP_API_KEY = os.getenv("SERP")

# Initialize triage system
triage = TriageSystem(data_path="data/", serp_api_key=SERP_API_KEY)

st.title("🩺 Symptom Checker & Triage System")

# Symptom input with auto-complete
all_symptoms = triage.all_symptoms
selected_symptoms = st.multiselect(
    "Select or type your symptoms:",
    options=all_symptoms,
    help="Start typing to search for a symptom."
)

if st.button("Run Triage"):
    if not selected_symptoms:
        st.warning("⚠️ Please select at least one symptom!")
    else:
        result = triage.assess_patient(selected_symptoms)

        st.subheader("📋 Triage Summary")
        st.write(f"✅ **Validated Symptoms:** {result['validated_symptoms']}")
        st.write(f"💥 **Risk Score:** {result['risk_score']}")
        st.write(f"⚠️ **Severity Level:** {result['severity_level']}")
        st.write(f"💡 **Care Recommendation:** {result['care_recommendation']}")

        st.subheader("🩺 Predicted Diseases and Details:")
        for detail in result['disease_details']:
            st.markdown(f"**➡ Disease:** {detail['disease'].capitalize()}")
            st.markdown(f"**Description:** {detail['description']}")
            st.markdown(f"**Precautions:** {detail['precautions']}")
            st.write("---")
