import streamlit as st
import os
from dotenv import load_dotenv
from symptom_checker.triage_system import TriageSystem

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Medical Symptom Checker",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Caching the Triage System ---
# Use st.cache_resource to load the model and data only once
@st.cache_resource
def load_triage_system():
    """
    Loads and caches the TriageSystem instance.
    This function will only be run once, when the app first starts.
    """
    print("--- Initializing Triage System for the first time ---")
    load_dotenv(dotenv_path='safe.env')
    serp_api_key = os.getenv("SERP_API_KEY")
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not serp_api_key or not groq_api_key:
        st.error("API Keys are missing! Please ensure 'safe.env' is configured.")
        return None
        
    try:
        system = TriageSystem(serp_api_key=serp_api_key, groq_api_key=groq_api_key)
        return system
    except Exception as e:
        st.error(f"Failed to initialize the system: {e}")
        return None

# --- Main Application UI ---
st.title("🩺 AI Medical Symptom Checker")
st.markdown(
    "Welcome! This tool helps you understand potential health conditions based on your symptoms. "
    "**This is not a substitute for professional medical advice.**"
)

# Load the system from cache
triage_system = load_triage_system()

if triage_system:
    # Get the list of all symptoms for the dropdown
    symptom_list = triage_system.all_symptoms
    
    # Replace underscores with spaces for better readability in the UI
    symptom_list_display = [s.replace('_', ' ').title() for s in symptom_list]

    st.subheader("Step 1: Select Your Symptoms")
    selected_symptoms_display = st.multiselect(
        "Start typing to search for symptoms...",
        options=symptom_list_display,
        help="You can select multiple symptoms."
    )

    # Convert display symptoms back to the format the model expects
    selected_symptoms_raw = [s.lower().replace(' ', '_') for s in selected_symptoms_display]

    st.subheader("Step 2: Get Assessment")
    if st.button("Assess My Symptoms", type="primary", use_container_width=True):
        if not selected_symptoms_raw:
            st.warning("Please select at least one symptom.")
        else:
            with st.spinner("Analyzing your symptoms..."):
                # Get the assessment from the backend
                result = triage_system.assess_patient(selected_symptoms_raw)

            if "error" in result:
                st.error(result["error"])
            else:
                st.subheader("📋 Assessment Report")

                # Display Care Recommendation with color-coding
                severity = result['severity_level']
                recommendation = result['care_recommendation']
                
                if severity == "HIGH":
                    st.error(f"**Care Recommendation: {recommendation}**")
                elif severity == "MEDIUM":
                    st.warning(f"**Care Recommendation: {recommendation}**")
                else:
                    st.info(f"**Care Recommendation: {recommendation}**")

                # Display Risk Score and Validated Symptoms in columns
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Calculated Risk Score", value=f"{result['risk_score']:.1f}")
                with col2:
                     with st.expander("See your validated symptoms"):
                        st.write(", ".join([s.replace('_', ' ').title() for s in result['validated_symptoms']]))


                st.divider()

                # Display Predicted Disease Details
                disease_info = result['predicted_disease']
                st.subheader(f"Most Likely Condition: {disease_info['name']}")
                
                st.markdown("**Description:**")
                st.write(disease_info['description'])

                st.markdown("**Suggested Precautions:**")
                # The RAG output is already in markdown format, so we can display it directly
                st.markdown(disease_info['precautions'])

else:
    st.error("The application could not be started. Please check the console for errors.")

