# services/data_cleaner.py
import pandas as pd

class DataCleaner:
    @staticmethod
    def clean_data(df):
        # Supprimez les lignes avec des valeurs manquantes
        df = df.dropna()
        
        # Convertissez les colonnes de date en format datetime
        date_columns = ['date', 'timestamp']  # Ajustez selon vos besoins
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        
        # Autres opérations de nettoyage spécifiques à vos données
        
        return df