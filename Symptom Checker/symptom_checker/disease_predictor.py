import pandas as pd
from sklearn.tree import DecisionTreeClassifier

class DiseasePredictor:
    _model_trained = False
    _model = None
    _symptom_columns = []

    @classmethod
    def train_model(cls, dataset):
        symptom_columns = [col for col in dataset.columns if col.startswith('Symptom_')]
        cls._symptom_columns = symptom_columns

        X = []
        y = []
        for _, row in dataset.iterrows():
            features = [1 if pd.notna(row[col]) and str(row[col]).strip() else 0 for col in symptom_columns]
            X.append(features)
            y.append(row['Disease'].strip().lower())

        clf = DecisionTreeClassifier(max_depth=10, random_state=42)
        clf.fit(X, y)

        cls._model = clf
        cls._model_trained = True

    @classmethod
    def predict(cls, symptoms, symptom_disease_map):
        if not cls._model_trained:
            print("rule-based prediction.")
            return cls.rule_based_predict(symptoms, symptom_disease_map)

        symptom_set = set(symptoms)
        features = [1 if col in symptom_set else 0 for col in cls._symptom_columns]

        prediction = cls._model.predict([features])[0]
        return [prediction]

    @staticmethod
    def rule_based_predict(symptoms, symptom_disease_map):
        disease_scores = {}
        for symptom in symptoms:
            for disease in symptom_disease_map.get(symptom, []):
                disease_scores[disease] = disease_scores.get(disease, 0) + 1

        sorted_diseases = sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)
        return [disease for disease, _ in sorted_diseases[:5]]
