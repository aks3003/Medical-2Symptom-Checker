class RiskAssessor:
    @staticmethod
    def calculate(validated_symptoms, severity_mapping):
        return sum(severity_mapping.get(symptom, 1) for symptom in validated_symptoms)
