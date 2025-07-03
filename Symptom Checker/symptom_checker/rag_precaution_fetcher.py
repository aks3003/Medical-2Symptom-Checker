from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

# === 📥 Load environment variables ===
load_dotenv(dotenv_path='C:/Users/akshi/OneDrive/Documents/Symptom Checker/symptom_checker/safe.env')
class RAGPrecautionFetcher:
    def __init__(self, serp_api_key=None):
        if serp_api_key is None:
            serp_api_key = os.getenv("SERP_API_KEY")
        if not serp_api_key:
            raise ValueError("SERP API key is missing! Set SERP_API_KEY in your .env file or pass as argument.")
        self.serp_api_key = serp_api_key
        self.cache = {}

    def query_serp_api(self, query):
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

    def fetch_precautions(self, disease):
        query = f"precautions for {disease}"
        results = self.query_serp_api(query)
        return self.simple_summarize_serp_results(results)

    def fetch_condition(self, symptoms):
        query = f"condition based on symptoms: {', '.join(symptoms)}"
        results = self.query_serp_api(query)
        return self.simple_summarize_serp_results(results)

    @staticmethod
    def simple_summarize_serp_results(results, top_n=3):
        if not results:
            return "No summary available."

        summaries = []
        for r in results[:top_n]:
            title = r.get('title', '')
            snippet = r.get('snippet', '')
            summaries.append(f"{title}: {snippet}".strip())

        return " | ".join(summaries) if summaries else "No summary available."


if __name__ == "__main__":
    try:
        fetcher = RAGPrecautionFetcher()

        disease = "flu"
        symptoms = ["fever", "cough"]

        print(f"\n🩺 Precautions for {disease}:")
        print(fetcher.fetch_precautions(disease))

        print(f"\n🩺 Condition summary for symptoms: {', '.join(symptoms)}")
        print(fetcher.fetch_condition(symptoms))

    except ValueError as ve:
        print(ve)
