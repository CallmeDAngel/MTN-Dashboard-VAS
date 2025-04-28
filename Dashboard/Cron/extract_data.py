# VAS_APP/Dashboard/Cron/extract_data.py
from django_cron import CronJobBase, Schedule
import openpyxl
import pandas as pd
import os
from datetime import datetime
import logging

# Configuration globale du logging
logging.basicConfig(filename=r'C:/Users/gael/OneDrive/Documents/Projet Soutenance/MTN_APP/VAS_APP/Dashboard/Cron/data_extractor.log', level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
def create_output_file_if_needed( filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if not os.path.exists(filename):
        pd.DataFrame().to_excel(filename, index=False, engine='openpyxl')
        logging.info(f"Fichier {filename} créé.")
    else:
        logging.info(f"Fichier {filename} existe déjà.")

def safe_read_excel( file_path, sheet_name):
    try:
        return pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl', parse_dates=True)
    except Exception as e:
        logging.error(f"Erreur lors de la lecture de {file_path}, feuille {sheet_name}: {str(e)}")
        return pd.DataFrame()

def safe_write_excel( df, file_path):
    try:
        for col in df.select_dtypes(include=['datetime64']).columns:
            df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

        with pd.ExcelWriter(file_path, engine='openpyxl', datetime_format='YYYY-MM-DD HH:MM:SS') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        logging.info(f"Données sauvegardées dans {file_path}")
    except Exception as e:
        logging.error(f"Erreur lors de l'écriture dans {file_path}: {str(e)}")

def convert_datetime_columns( df):
    for col in df.select_dtypes(include=['datetime64']).columns:
        df[col] = pd.to_datetime(df[col], errors='coerce', format='%Y-%m-%d %H:%M:%S')
    return df

def extract_data( input_file, output_normal, output_detail):
    try:
        
        wb = openpyxl.load_workbook(input_file)
        for sheet in wb.sheetnames:
            logging.info(f"Traitement de la feuille: {sheet}")

            if sheet.lower() == "details" or "error" not in sheet.lower():
                df = safe_read_excel(input_file, sheet_name=sheet)

                if df.empty:
                    logging.info(f"La feuille {sheet} est vide. Ignorer.")
                    continue

                if sheet.lower() == "details":
                    logging.info("Extraction des données de la feuille 'détail'.")
                    create_output_file_if_needed(output_detail)
                    safe_write_excel(df, output_detail)
                else:
                    create_output_file_if_needed(output_normal)
                    existing_data = safe_read_excel(output_normal, sheet_name='Sheet1')
                    df = convert_datetime_columns(df)
                    if not existing_data.empty:
                        existing_data = convert_datetime_columns(existing_data)

                    updated_data = pd.concat([existing_data, df], ignore_index=True)
                    updated_data.drop_duplicates(inplace=True)

                    safe_write_excel(updated_data, output_normal)

    except Exception as e:
        logging.error(f"Erreur lors du traitement du fichier {input_file}: {str(e)}")

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every miniute
    RETRY_AFTER_FAILURE_MINS = 1
    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    # RUN_AT_TIMES = ['04:30', '14:30']  # Exécuter toutes les 1 minute

    # schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'Dashboard.Cron.extract_data.MyCronJob'  # Un code unique pour identifier cette tâche


    def do(self):
        print("test cron")
        input_file = "C:/Users/gael/OneDrive/Documents/Projet Soutenance/MTN_APP/VAS_APP/Dashboard/static/StatsMoMos 2024.xlsx"
        output_normal = "C:/Users/gael/OneDrive/Documents/Projet Soutenance/MTN_APP/VAS_APP/Dashboard/static/xlxs/donnees_normales.xlsx"
        output_detail = "C:/Users/gael/OneDrive/Documents/Projet Soutenance/MTN_APP/VAS_APP/Dashboard/static/xlxs/donnees_detail.xlsx"

        if os.path.exists(input_file):
            logging.info(f"Extraction commencée à {datetime.now()}")
            extract_data(input_file, output_normal, output_detail)
        else:
            logging.warning(f"Le fichier {input_file} n'existe pas.")
