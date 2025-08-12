from symptom_checker.disease_predictor import DiseasePredictor
from serpapi import GoogleSearch
from groq import Groq
from dotenv import load_dotenv
import os

# === Load environment variables ===
load_dotenv(dotenv_path='C:/Users/akshi/OneDrive/Documents/Symptom Checker/symptom_checker/safe.env')

class RAGPrecautionFetcher:
    def __init__(self, serp_api_key=None, groq_api_key=None):
        self.serp_api_key = serp_api_key or os.getenv("SERP_API_KEY")
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")

        if not self.serp_api_key:
            raise ValueError("❌ SERP API key is missing!")
        if not self.groq_api_key:
            raise ValueError("❌ GROQ API key is missing!")

        self.client = Groq(api_key=self.groq_api_key)
        self.cache = {}

    def query_serp_api(self, query):
        """Query SERP API (DuckDuckGo engine)"""
        if query in self.cache:
            return self.cache[query]

        params = {
            'q': query,
            'api_key': self.serp_api_key,
            'engine': 'duckduckgo'
        }
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            organic_results = results.get('organic_results', [])
            self.cache[query] = organic_results
            return organic_results
        except Exception as e:
            print(f"❌ SERP API query failed: {e}")
            return []

    def summarize_with_groq(self, snippets):
        """Send SERP snippets to Groq for clean summarization"""
        if not snippets:
            return "No relevant precautions found."

        prompt = f"Based on the following sources, summarize key medical precautions in simple points:\n\n{snippets}"
        try:
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ Groq summarization failed: {e}")
            return "Summary unavailable due to API error."

    def fetch_precautions(self, disease):
        """Fetch & summarize precautions for a predicted disease"""
        query = f"precautions for {disease}"
        results = self.query_serp_api(query)
        snippets = " ".join([r.get("snippet", "") for r in results[:5]])
        return self.summarize_with_groq(snippets)

# ======= Example Standalone Run =======
if __name__ == "__main__":
    # Example patient symptoms
    patient_symptoms = ["fever", "cough", "body pain"]

    # Dummy mapping for rule-based fallback (if model not trained)
    symptom_disease_map = {
        "fever": ["flu", "dengue"],
        "cough": ["flu", "bronchitis"],
        "body pain": ["flu", "dengue"]
    }

    # Predict disease
    predicted_diseases = DiseasePredictor.predict(patient_symptoms, symptom_disease_map)
    predicted_disease = predicted_diseases[0] if predicted_diseases else "Unknown"

    print(f"🩺 Predicted Disease: {predicted_disease}")

    # Fetch precautions via RAG + Groq
    fetcher = RAGPrecautionFetcher()
    precautions_summary = fetcher.fetch_precautions(predicted_disease)

    print(f"\n💡 Precautions for {predicted_disease}:\n{precautions_summary}")
