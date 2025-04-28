import pandas as pd

def read_excel_file(file_path, sheet_name):
    # Lire le fichier Excel
    df = pd.read_excel('D:/MEVO Kpossou/Documents/CDI Daily Report 2024.xlsx', sheet_name = 'Application_Statuts' )
    return df

def extract_kpi_data(df):
    QOS = (df['P2P Success']/df['P2P Total']) * 100
    UR = df['KPI_Column_2'].mean()
    # Ajouter d'autres KPI selon vos besoins
    return {'kpi1': QOS, 'kpi2': UR}
