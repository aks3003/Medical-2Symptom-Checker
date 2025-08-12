
# 🩺 Medical Symptom Checker

An intelligent **medical triage and disease prediction system** powered by:
- ✅ Machine learning (Decision Tree)
- ✅ Rule-based reasoning
- ✅ Retrieval-Augmented Generation (RAG) using SerpAPI and GROQ
- ✅ Streamlit interactive web app

---

## 🚀 Features

- 🌟 **Symptom validation & risk assessment**  
- 🌟 **Severity classification (LOW / MEDIUM / HIGH)**  
- 🌟 **Care recommendations (e.g., SELF CARE, CONSULT DOCTOR)**  
- 🌟 **Disease prediction (ML + rule-based fallback)**  
- 🌟 **Precautions & condition info fetched live via SerpAPI (RAG)**  
- 🌟 **User-friendly Streamlit app for real-time triage**

---

## 🏗 Tech Stack

| Component    | Technology                 |
|--------------|---------------------------|
| ML Model     | Scikit-Learn Decision Tree |
| Web App      | Streamlit                  |
| RAG Fetcher  | SerpAPI + Groq             |
| Data Handling| Pandas                     |
| Deployment   | Streamlit, GitHub          |

---

## 📂 Project Structure

```
Medical-Symptom-Checker/
├── data/                  # Medical datasets (symptoms, severity, etc.)
├── symptom_checker/        # Core logic modules (triage, ML, RAG, etc.)
├── app.py                  # Streamlit frontend
├── main.py                 # CLI runner
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## ⚡ How to Run

### 1️⃣ Clone the repository
```bash
git clone https://github.com/aks3003/Medical-Symptom-Checker.git
cd Medical-Symptom-Checker
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set up environment
Create a `.env` or `safe.env` file with your **SERPAPI key**:
```
SERP=your_serpapi_key
GROQ=your_GROQ_key
```

### 4️⃣ Run the Streamlit app
```bash
streamlit run app.py
```

### 5️⃣ Or run via CLI
```bash
python main.py
```

---

## 📊 Example Output

```
📋 Triage Summary
✅ Validated Symptoms: ['fever', 'cough']
💥 Risk Score: 10
⚠️ Severity Level: MEDIUM
💡 Care Recommendation: CONSULT DOCTOR

🩺 Predicted Diseases and Details:
➡ Disease: pneumonia
   Description: Pneumonia is an infection of the lungs...
   Precautions: Get vaccinated, wash hands, avoid smoking...
```

---

## 🔒 Notes

- This tool is for **educational/demo purposes only** and not a replacement for professional medical advice.
- API keys (e.g., SerpAPI) should be kept secure in `.env`.

---

## 💡 Future Improvements

- Add support for other ML models (e.g., XGBoost)
- Use GROQ API for richer RAG summarization
- Dockerize for easy deployment

---

## 🙌 Credits

Built with ❤️ by [aks3003](https://github.com/aks3003)

---
