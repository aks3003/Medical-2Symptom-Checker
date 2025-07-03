import pandas as pd
from sklearn.tree import DecisionTreeClassifier

class MedicalDataLoader:
    """Loads and processes the actual medical datasets"""

    def __init__(self, data_path='data/'):
        self.data_path = data_path
        self.datasets = {}
        self.processed_data = {}

    def load_datasets(self):
        """Load all CSV files from the dataset"""
        print("🔄 Loading Medical Datasets...")

        try:
            self.datasets['main'] = pd.read_csv(f'{self.data_path}dataset.csv')
            self.datasets['descriptions'] = pd.read_csv(f'{self.data_path}symptom_Description.csv')
            self.datasets['precautions'] = pd.read_csv(f'{self.data_path}symptom_precaution.csv')
            self.datasets['severity'] = pd.read_csv(f'{self.data_path}symptom_severity.csv')

            print("✅ All datasets loaded successfully!")

            self._process_datasets()
            self.train_disease_model()

        except FileNotFoundError as e:
            print(f"❌ Error loading datasets: {e}")
            print("Creating fallback data structure...")
            self._create_fallback_data()

    def _process_datasets(self):
        """Process datasets into usable structures"""
        print("🔧 Processing datasets for triage system...")

        main_df = self.datasets['main']
        symptom_columns = [col for col in main_df.columns if col.startswith('Symptom_')]

        symptom_disease_map = {}
        all_symptoms = set()

        for _, row in main_df.iterrows():
            disease = row['Disease'].strip().lower()

            for col in symptom_columns:
                symptom_raw = row.get(col)
                if pd.notna(symptom_raw) and str(symptom_raw).strip():
                    symptom = str(symptom_raw).strip().lower().replace(' ', '_').replace('__', '_')
                    all_symptoms.add(symptom)

                    if symptom not in symptom_disease_map:
                        symptom_disease_map[symptom] = []
                    symptom_disease_map[symptom].append(disease)

        self.processed_data['all_symptoms'] = sorted(list(all_symptoms))
        self.processed_data['symptom_disease_map'] = symptom_disease_map

        severity_df = self.datasets['severity']
        severity_mapping = {}

        for _, row in severity_df.iterrows():
            symptom = row['Symptom'].strip().lower().replace(' ', '_').replace('__', '_')
            weight = row['weight']
            severity_mapping[symptom] = float(weight)

        self.processed_data['severity_mapping'] = severity_mapping

        precaution_df = self.datasets['precautions']
        precaution_mapping = {}

        for _, row in precaution_df.iterrows():
            disease = row['Disease'].strip().lower()
            precautions = []
            for i in range(1, 5):
                precaution_col = f'Precaution_{i}'
                if precaution_col in row and pd.notna(row[precaution_col]):
                    precautions.append(row[precaution_col].strip())
            precaution_mapping[disease] = precautions

        self.processed_data['precaution_mapping'] = precaution_mapping

        if 'descriptions' in self.datasets:
            desc_df = self.datasets['descriptions']
            description_mapping = {}
            for _, row in desc_df.iterrows():
                disease = row['Disease'].strip().lower()
                description = row['Description'] if 'Description' in row else ""
                description_mapping[disease] = description
            self.processed_data['description_mapping'] = description_mapping

        disease_symptom_map = {}
        for _, row in main_df.iterrows():
            disease = row['Disease'].strip().lower()
            symptoms = []
            for col in symptom_columns:
                symptom_raw = row.get(col)
                if pd.notna(symptom_raw) and str(symptom_raw).strip():
                    symptom = str(symptom_raw).strip().lower().replace(' ', '_').replace('__', '_')
                    symptoms.append(symptom)
            disease_symptom_map[disease] = symptoms

        self.processed_data['disease_symptom_map'] = disease_symptom_map

        print(f"✅ Processed {len(all_symptoms)} unique symptoms")
        print(f"✅ Processed {len(main_df['Disease'].unique())} diseases")
        print(f"✅ Processed {len(severity_mapping)} severity mappings")

    def train_disease_model(self):
        """Train a Decision Tree model to predict diseases from symptoms"""
        print("⚙️ Training Decision Tree Classifier...")

        main_df = self.datasets['main']
        symptom_columns = [col for col in main_df.columns if col.startswith('Symptom_')]
        all_symptoms = self.processed_data['all_symptoms']
        symptom_index = {symptom: i for i, symptom in enumerate(all_symptoms)}

        X = []
        y = []

        for _, row in main_df.iterrows():
            features = [0] * len(all_symptoms)
            for col in symptom_columns:
                symptom_raw = row.get(col)
                if pd.notna(symptom_raw) and str(symptom_raw).strip():
                    symptom = str(symptom_raw).strip().lower().replace(' ', '_').replace('__', '_')
                    if symptom in symptom_index:
                        features[symptom_index[symptom]] = 1
            X.append(features)
            y.append(row['Disease'].strip().lower())

        clf = DecisionTreeClassifier()
        clf.fit(X, y)

        self.processed_data['disease_model'] = clf
        print("✅ Disease prediction model trained!")

    def _create_fallback_data(self):
        """Fallback data if CSV files aren't available"""
        print("📋 Creating fallback dataset...")

        self.processed_data['severity_mapping'] = {
            'fever': 6.0, 'headache': 4.0, 'cough': 3.0, 'shortness_of_breath': 8.0,
            'chest_pain': 9.0, 'nausea': 4.0, 'vomiting': 5.0, 'diarrhea': 4.0
        }

        self.processed_data['all_symptoms'] = list(self.processed_data['severity_mapping'].keys())

        self.processed_data['symptom_disease_map'] = {
            'fever': ['common_cold', 'flu', 'pneumonia'],
            'headache': ['migraine', 'flu']
        }

        self.processed_data['precaution_mapping'] = {
            'common_cold': ['rest', 'stay hydrated'],
            'flu': ['rest', 'stay hydrated', 'antiviral medication']
        }

        print("✅ Fallback data created")
