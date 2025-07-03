class CareRecommender:
    @staticmethod
    def recommend(severity_level):
        if severity_level == "HIGH":
            return "IMMEDIATE MEDICAL ATTENTION"
        elif severity_level == "MEDIUM":
            return "CONSULT DOCTOR"
        else:
            return "SELF CARE"
