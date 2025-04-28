import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import logging

# Configurer les logs
logging.basicConfig(filename='scraping.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_headers(table):
    try:
        headers = [
            header.text for header in table.find_elements(By.XPATH, '//*[@id="app"]/main/div[2]/div/div/section/main/div/div[3]/div/div[2]/table/thead/tr/th[position() >= 2 and position() <= 5]')
        ]
        logging.info(f"En-tête récupérée : {headers}")
        return headers
    except Exception as e:
        logging.error(f"Erreur lors de l'extraction des en-têtes : {e}")
        return []

def extract_rows(table):
    try:
        rows = []
        for row in table.find_elements(By.XPATH, '/html/body/section/main/div[2]/div/div/section/main/div/div[3]/div/div[3]/table/tbody/tr'):
            cells = row.find_elements(By.XPATH, 'td[position() >= 2 and position() <= 5]')
            if cells:
                rows.append([cell.text for cell in cells])
        logging.info(f"Lignes récupérées : {rows}")
        return rows
    except Exception as e:
        logging.error(f"Erreur lors de l'extraction des lignes : {e}")
        return []

def extract_table_data(driver):
    all_rows = []
    page = 1
    headers = []

    while True:
        try:
            logging.info(f"Extraction des données de la page {page}")

            # Attendre que le tableau soit chargé
            table = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="app"]/main/div[2]/div/div/section/main/div/div[3]/div'))
            )
            logging.info(f"Tableau trouvé sur la page {page}")

            # Extraire les en-têtes de colonnes (seulement sur la première page)
            if page == 1:
                headers = extract_headers(table)

            # Extraire les lignes de données
            rows = extract_rows(table)
            all_rows.extend(rows)

            # Vérifier et passer à la page suivante
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/main/div[2]/div/div/section/main/div/div[1]/div[2]/div/button[2]'))
            )

            if "disabled" in next_button.get_attribute("class"):
                logging.info("Bouton Suivant désactivé. Pagination terminée.")
                break
            else:
                logging.info(f"Clic sur le bouton Suivant pour aller à la page {page + 1}")
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(2)
                page += 1

        except Exception as e:
            logging.error(f"Erreur lors de la récupération des données de la page {page}: {e}")
            break

    logging.info(f"Nombre total de lignes récupérées : {len(all_rows)}")
    return all_rows, headers

def main(url):
    try: 
        driver.get(url)
        time.sleep(5)  # Attendre que la page se charge

        # Connexion à la plateforme
        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        username.send_keys("kpossou")
        password.send_keys("Password007")
        driver.find_element(By.CSS_SELECTOR, "#app > main > div > div > div > form > div:nth-child(2) > button").click()
        time.sleep(5)  # Attendre que la page se charge

        # Extraire les données
        all_rows, headers = extract_table_data(driver)

        # Enregistrer les données dans un fichier Excel
        df = pd.DataFrame(all_rows, columns=headers)
        df.to_excel('table_data_edge.xlsx', index=False)
        logging.info("Les données du tableau ont été enregistrées dans 'table_data_edge.xlsx'.")
    
    except Exception as e:
        logging.error(f"Une erreur s'est produite : {e}")

# Configuration pour exécuter Selenium sans interface graphique
edge_option = Options()
edge_option.add_argument("--headless")  # Mode headless pour accélérer
edge_option.add_argument("--disable-gpu")  # Désactiver le GPU pour éviter certains problèmes de rendu
driver_path = "D:/MEVO Kpossou/Downloads/edgedriver_win64/msedgedriver.exe"
driver = webdriver.Edge(service=Service(driver_path), options=edge_option)

url = "http://10.10.50.9/#/hdm/cpe"
main(url)
