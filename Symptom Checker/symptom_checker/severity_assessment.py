class SeverityAssessor:
    @staticmethod
    def classify(risk_score):
        if risk_score >= 12:
            return "HIGH"
        elif risk_score >= 8:
            return "MEDIUM"
        else:
            return "LOW"
