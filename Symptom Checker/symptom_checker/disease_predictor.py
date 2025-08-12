# symptom_checker/disease_predictor.py
from sklearn.tree import DecisionTreeClassifier

class DiseasePredictor:
    """A classifier to predict diseases based on symptoms."""
    
    def __init__(self, random_state=42):
        self.model = DecisionTreeClassifier(random_state=random_state)
        self.symptom_columns = []
        self._is_trained = False

    def train(self, X_train, y_train):
        """Trains the Decision Tree model."""
        print("⚙️ Training Decision Tree Classifier for disease prediction...")
        self.symptom_columns = X_train.columns.tolist()
        self.model.fit(X_train, y_train)
        self._is_trained = True
        print("✅ Disease prediction model trained!")

    def predict(self, symptoms):
        """Predicts the disease from a list of validated symptoms."""
        if not self._is_trained:
            raise RuntimeError("Model has not been trained yet. Call train() first.")
        
        # Create a zero-vector based on the training columns
        input_vector = {symptom: 0 for symptom in self.symptom_columns}
        
        # Set the patient's symptoms to 1
        for symptom in symptoms:
            if symptom in input_vector:
                input_vector[symptom] = 1
        
        # Convert to list in the correct order for prediction
        ordered_input = [input_vector[symptom] for symptom in self.symptom_columns]
        
        prediction = self.model.predict([ordered_input])
        return prediction[0] # Returns the single predicted disease name
