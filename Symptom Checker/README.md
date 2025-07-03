# 🩺 Medical Symptom Checker and Triage System

## 🔍 Project Overview

This project is an **AI-assisted Medical Symptom Checker and Triage System** designed to help users assess their symptoms and receive preliminary medical insights. It leverages both rule-based logic and machine learning to predict diseases and provide appropriate care recommendations.

The system performs:
- Symptom validation
- Disease prediction using a Decision Tree Classifier
- Risk scoring based on severity
- Severity classification
- Care recommendations
- Disease description and precaution retrieval

## 🎯 Problem Statement

> **Build an AI system that takes patient symptoms and provides preliminary risk assessment and care recommendations.**

## ✅ Key Features

- ✔️ **Symptom Validation:** Ensures only valid symptoms are processed.
- ✔️ **Disease Prediction:** Maps symptoms to diseases using rule-based logic and an ML model.
- ✔️ **Risk Assessment:** Calculates risk based on symptom severity and combinations.
- ✔️ **Severity Classification:** Categorizes the risk into LOW, MODERATE, HIGH, or CRITICAL.
- ✔️ **Care Recommendations:** Suggests **Self Care**, **Primary Care**, **Urgent Care**, or **Emergency Care**.
- ✔️ **Disease Info:** Provides descriptions and recommended precautions for each predicted disease.
- ✔️ **Modular Code:** Each component (validation, risk, care, ML, etc.) is separated for maintainability.

## 🔬 Tech Stack

- **Language:** Python 3.x
- **ML Library:** scikit-learn (Decision Tree Classifier)
- **Data Processing:** pandas
- **Dataset:** Kaggle Disease Symptom Dataset

## 📊 Dataset

[Kaggle Dataset Link](https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset)

Files used:
- `dataset.csv`: Diseases & their associated symptoms
- `symptom_severity.csv`: Severity of each symptom
- `symptom_precaution.csv`: Precautions for each disease
- `symptom_Description.csv`: Disease descriptions

## 🔑 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/your-username/medical-symptom-checker.git
cd medical-symptom-checker
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Dataset
Place all dataset `.csv` files in the `/data/` directory.

### 4. Run the project
```bash
python main.py
```

## 📋 Example Output

```
🔬 MIGRAINE:
 - Description: A migraine causes severe throbbing head pain, nausea, and light sensitivity.
 - Precautions: meditation, reduce stress, use polaroid glasses in sun, consult doctor

📋 Final Assessment Summary:
- Validated Symptoms: ['headache', 'cough']
- Predicted Diseases: ['migraine', 'common_cold', 'flu']
- Risk Score: 7.0
- Severity Level: LOW
- Care Recommendation: SELF CARE
```

## 💡 Architecture Flow

```
[User Symptoms]
       ↓
[Symptom Validation]
       ↓
[ML & Rule-based Disease Prediction]
       ↓
[Risk Scoring & Symptom Severity]
       ↓
[Severity Classification]
       ↓
[Care Recommendation + Disease Description + Precautions]
```

## 🛡️ Skills Demonstrated

| Skill Area            | Description                                                                      |
|-----------------------|----------------------------------------------------------------------------------|
| **AI/ML**             | Built a Decision Tree Classifier on real symptom-disease data                    |
| **Critical Thinking** | Balanced risk scoring, handled multi-condition overlap                          |
| **Problem Solving**   | Resolved symptom ambiguity, incomplete symptom cases                             |
| **Modular Code**      | Created isolated modules for validation, ML, risk, care recommendation           |
| **Architecture**      | Designed a clean flow from symptom input → triage output                         |

## 🚀 Future Scope

- ✅ Build a Web Interface (Flask/FastAPI)
- ✅ Add more ML models (Random Forest, Naive Bayes)
- ✅ Build a patient history tracking system
- ✅ Add NLP support for free-text symptom input
- ✅ Deploy as a cloud API for integration

## 🤝 Acknowledgements

- Dataset: [Kaggle - Disease Symptom Dataset](https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset)
- Python open-source community
- scikit-learn, pandas

## 📜 License

This project is open-source under the MIT License.
