# symptom_checker/data_loader.py
import pandas as pd

class MedicalDataLoader:
    """Loads and processes the medical datasets."""

    def __init__(self, data_path='data/'):
        self.data_path = data_path
        self.datasets = {}
        self.processed_data = {}

    def load_and_process_data(self):
        """Load all CSV files and process them into usable structures."""
        print("🔄 Loading and Processing Medical Datasets...")
        try:
            self.datasets['main'] = pd.read_csv(f'{self.data_path}dataset.csv')
            self.datasets['descriptions'] = pd.read_csv(f'{self.data_path}symptom_Description.csv')
            self.datasets['precautions'] = pd.read_csv(f'{self.data_path}symptom_precaution.csv')
            self.datasets['severity'] = pd.read_csv(f'{self.data_path}symptom_severity.csv')
            print("✅ All datasets loaded successfully!")
            self._process_datasets()
        except FileNotFoundError as e:
            print(f"❌ Error loading datasets: {e}")
            # You could add a fallback mechanism here if needed
            raise

    def _process_datasets(self):
        """Process raw DataFrames into application-ready dictionaries and lists."""
        main_df = self.datasets['main']
        symptom_columns = [col for col in main_df.columns if col.startswith('Symptom_')]

        # Create a comprehensive list of all unique symptoms
        all_symptoms_set = set()
        for col in symptom_columns:
            main_df[col] = main_df[col].str.strip().str.lower().str.replace(' ', '_').replace('__', '_')
            all_symptoms_set.update(main_df[col].dropna().unique())
        
        all_symptoms = sorted(list(all_symptoms_set))
        self.processed_data['all_symptoms'] = all_symptoms
        symptom_index = {symptom: i for i, symptom in enumerate(all_symptoms)}

        # Prepare data for model training (X, y)
        X = []
        y = []
        for _, row in main_df.iterrows():
            features = [0] * len(all_symptoms)
            for col in symptom_columns:
                symptom = row.get(col)
                if pd.notna(symptom) and symptom in symptom_index:
                    features[symptom_index[symptom]] = 1
            X.append(features)
            y.append(row['Disease'].strip().lower())

        self.processed_data['X_train'] = pd.DataFrame(X, columns=all_symptoms)
        self.processed_data['y_train'] = pd.Series(y)
        
        # Process severity mapping
        severity_df = self.datasets['severity']
        severity_mapping = {}
        for _, row in severity_df.iterrows():
            symptom = row['Symptom'].strip().lower().replace(' ', '_').replace('__', '_')
            severity_mapping[symptom] = float(row['weight'])
        self.processed_data['severity_mapping'] = severity_mapping

        # Process precaution mapping (from local CSV)
        precaution_df = self.datasets['precautions']
        precaution_mapping = {}
        for _, row in precaution_df.iterrows():
            disease = row['Disease'].strip().lower()
            precautions = [row[f'Precaution_{i}'].strip() for i in range(1, 5) if f'Precaution_{i}' in row and pd.notna(row[f'Precaution_{i}'])]
            precaution_mapping[disease] = precautions
        self.processed_data['precaution_mapping'] = precaution_mapping
        
        # Process description mapping
        desc_df = self.datasets['descriptions']
        description_mapping = {}
        for _, row in desc_df.iterrows():
            disease = row['Disease'].strip().lower()
            description_mapping[disease] = row.get('Description', "").strip()
        self.processed_data['description_mapping'] = description_mapping

        print(f"✅ Processed {len(all_symptoms)} unique symptoms and prepared data for model training.")
        
    def get_processed_data(self):
        """Returns all the processed data structures."""
        return self.processed_data
