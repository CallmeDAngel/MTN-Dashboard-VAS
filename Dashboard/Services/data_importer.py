import pandas as pd

class DataImporter:
    @staticmethod
    def import_data(data_source_id):
        from Dashboard.models import DataSource
        data_source = DataSource.objects.get(id=data_source_id)
        if data_source.type_source == 'excel':
            df = pd.read_excel(data_source.file.path)
        elif data_source.type_source == 'csv':
            df = pd.read_csv(data_source.file.path)
        else:
            raise ValueError(f"Unsupported data source type: {data_source.type_source}")
        
        return df