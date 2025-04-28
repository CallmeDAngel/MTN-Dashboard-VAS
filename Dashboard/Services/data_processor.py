# services/data_processor.py
from .data_importer import DataImporter
from .data_cleaner import DataCleaner
from .kpi_calculator import KPICalculator

class DataProcessor:
    def __init__(self, data_source_id):
        from ..models import DataSource
        self.data_source = DataSource.objects.get(id=data_source_id)
        self.platform = self.data_source.platform

    def process(self):
        # Importer les données
        raw_data = DataImporter.import_data(self.data_source.id)
        
        # Nettoyer les données
        clean_data = DataCleaner.clean_data(raw_data)
        
        # Calculer les KPIs
        self.calculate_and_update_kpis(clean_data)
        
        # Sauvegarder les données historiques
        self.save_historical_data(clean_data)

    def calculate_and_update_kpis(self, data):
        from ..models import KPI
        kpi_types = ['QOS', 'USAGE_RATE']
        for kpi_type in kpi_types:
            value = KPICalculator.calculate(kpi_type, self.platform.name, data)
            KPI.objects.update_or_create(
                nom=kpi_type,
                platform=self.platform,
                defaults={'valeur': value}
            )

    def save_historical_data(self, data):
        from ..models import HistoricalData
        HistoricalData.objects.create(
            platform=self.platform,
            date=data['date'].max(),  # Supposons que 'date' est une colonne dans vos données
            data=data.to_dict()
        )