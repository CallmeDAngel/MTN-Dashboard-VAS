import openpyxl
import pandas as pd
import os
import time
from datetime import datetime
import logging

# Configuration du logging
logging.basicConfig(filename='data_extractor.log', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')


def create_output_file_if_needed(filename):
    # Créer le répertoire parent si nécessaire
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    if not os.path.exists(filename):
        pd.DataFrame().to_excel(filename, index=False, engine='openpyxl')
        logging.info(f"Fichier {filename} créé.")
    else:
        logging.info(f"Fichier {filename} existe déjà.")


def safe_read_excel(file_path, sheet_name):
    try:
        # Utiliser 'openpyxl' comme moteur et spécifier que les dates doivent être analysées
        return pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl', parse_dates=True)
    except Exception as e:
        logging.error(f"Erreur lors de la lecture de {file_path}, feuille {sheet_name}: {str(e)}")
        return pd.DataFrame()


def safe_write_excel(df, file_path):
    try:
        # Convertir les colonnes de type datetime en chaînes de caractères avant écriture
        for col in df.select_dtypes(include=['datetime64']).columns:
            df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

        with pd.ExcelWriter(file_path, engine='openpyxl', datetime_format='YYYY-MM-DD HH:MM:SS') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        logging.info(f"Données sauvegardées dans {file_path}")
    except Exception as e:
        logging.error(f"Erreur lors de l'écriture dans {file_path}: {str(e)}")


def convert_datetime_columns(df):
    """ Convertit les colonnes de type datetime dans le DataFrame. """
    for col in df.select_dtypes(include=['datetime64']).columns:
        df[col] = pd.to_datetime(df[col], errors='coerce', format='%Y-%m-%d %H:%M:%S')
    return df


def extract_data(input_file, output_normal, output_detail):
    """ Extrait les données du fichier Excel et les sauvegarde dans les fichiers de sortie. """
    try:
        wb = openpyxl.load_workbook(input_file)
        for sheet in wb.sheetnames:
            logging.info(f"Traitement de la feuille: {sheet}")

            # Limiter aux feuilles 'détail' et celles ne contenant pas 'error' dans leur nom
            if sheet.lower() == "détail" or "error" not in sheet.lower():
                df = safe_read_excel(input_file, sheet_name=sheet)

                if df.empty:
                    logging.info(f"La feuille {sheet} est vide. Ignorer.")
                    continue

                if sheet.lower() == "details":
                    # Extraction spécifique pour la feuille "détail"
                    logging.info(f"Extraction des données de la feuille 'détail'.")
                    create_output_file_if_needed(output_detail)
                    safe_write_excel(df, output_detail)
                else:
                    # Traitement des données normales
                    create_output_file_if_needed(output_normal)

                    existing_data = safe_read_excel(output_normal, sheet_name='Sheet1')

                    # Convertir explicitement les colonnes de type datetime
                    df = convert_datetime_columns(df)
                    if not existing_data.empty:
                        existing_data = convert_datetime_columns(existing_data)

                    updated_data = pd.concat([existing_data, df], ignore_index=True)
                    updated_data.drop_duplicates(inplace=True)

                    safe_write_excel(updated_data, output_normal)

    except Exception as e:
        logging.error(f"Erreur lors du traitement du fichier {input_file}: {str(e)}")


def main():
    input_file = "C:/Users/gael/OneDrive/Documents/Projet Soutenance/MTN_APP/VAS_APP/Dashboard/static/StatsMoMo 2024.xlsx"
    output_normal = "C:/Users/gael/OneDrive/Documents/Projet Soutenance/MTN_APP/VAS_APP/Dashboard/static/xlxsdonnees_normales.xlsx"
    output_detail = "C:/Users/gael/OneDrive/Documents/Projet Soutenance/MTN_APP/VAS_APP/Dashboard/static/xlxsdonnees_detail.xlsx"

    while True:
        try:
            if os.path.exists(input_file):
                logging.info(f"Extraction commencée à {datetime.now()}")
                extract_data(input_file, output_normal, output_detail)
            else:
                logging.warning(f"Le fichier {input_file} n'existe pas. Vérification suivante dans 1 minute.")
            time.sleep(60)  # Attendre 1 minute
        except KeyboardInterrupt:
            logging.info("Programme interrompu par l'utilisateur.")
            break
        except Exception as e:
            logging.error(f"Une erreur inattendue s'est produite: {str(e)}")
            time.sleep(10)  # Attendre 10 secondes avant de réessayer


if __name__ == "__main__":
    main()
