class SymptomValidator:
    @staticmethod
    def validate(symptoms, all_symptoms):
        validated = []
        for symptom in symptoms:
            norm_symptom = symptom.strip().lower().replace(' ', '_')
            if norm_symptom in all_symptoms:
                validated.append(norm_symptom)
        return validated
