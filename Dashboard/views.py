import logging
import os
from django.shortcuts import redirect, render
import pandas as pd
from django.http import JsonResponse 
from django.conf import settings
from .models import Notification
from django.contrib.auth.decorators import login_required

Logger = logging.getLogger(__name__)

# Create your views here.
def get_sheets(request):
    excel_file = 'Dashboard/static/xlxs/StatsMoMo 2024.xlsx'
    xls = pd.ExcelFile(excel_file)
    sheets = xls.sheet_names

    # Filtrer les feuilles ne contenant pas "error"
    filtered_sheets = [sheet for sheet in sheets if "error" not in sheet.lower()]

    return JsonResponse({'sheets': filtered_sheets})

def get_sheets_error(request):
    excel_file = 'Dashboard/static/StatsMoMo 2024.xlsx'
    xls = pd.ExcelFile(excel_file)
    sheets = xls.sheet_names

    # Filtrer les feuilles contenant "error"
    filtered_sheets = [sheet for sheet in sheets if "error" in sheet.lower()]

    return JsonResponse({'sheets': filtered_sheets})

#Acceuil
@login_required
def extract_month_year(sheet_name):
    try:
        # Gestion des noms de feuilles avec mois et année
        if 'error' in sheet_name:
            sheet_name = sheet_name.replace(' error', '')

        # Traitement des formats 'Jan 24', 'Feb 24', etc.
        if ' ' in sheet_name and len(sheet_name.split()) == 2:
            month, year = sheet_name.split()
            month = pd.to_datetime(month, format='%b', errors='coerce').month
            year = f"20{year}"
        else:
            # Traitement des formats 'Janvier', 'Février', etc.
            month_str = sheet_name.split()[0]
            month = pd.to_datetime(month_str, format='%B', errors='coerce').month
            year = '2024'  # Utiliser une année par défaut si non précisée

        return int(year), int(month)
    except Exception as e:
        print(f"Erreur lors de l'extraction du mois et de l'année : {e}")
        return 2024, 1  # Valeur par défaut en cas d'erreur

def get_latest_sheet(file_path):
    # Charger le fichier Excel pour obtenir toutes les feuilles
    xls = pd.ExcelFile(file_path)
    return xls.sheet_names[-1]  # Retourne le dernier nom de feuille

def get_previous_sheet(file_path, current_sheet):
    # Charger le fichier Excel pour obtenir toutes les feuilles
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names

    # Trouver l'index de la feuille actuelle
    current_index = sheet_names.index(current_sheet)

    # Si la feuille actuelle est la première, retourner None ou une autre valeur par défaut
    if current_index == 0:
        return None

    # Retourner la feuille précédente
    return sheet_names[current_index - 1]

def acceuil(request):
    return render(request, 'dashboard/acceuil.html')

def acceuil_pie(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Success_A2P', 'Error_A2P', 'Total']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Calculer les valeurs totales
        success_total = df['Success_A2P'].sum()
        error_total = df['Error_A2P'].sum()
        grand_total = df['Total'].sum()

        # Calculer les pourcentages
        success_percentage = (success_total / grand_total) * 100 if grand_total else 0
        error_percentage = (error_total / grand_total) * 100 if grand_total else 0
        # Le reste est la différence jusqu'à 100%
        # remaining_percentage = 100 - success_percentage - error_percentage
        
        # Arrondir les pourcentages au dixième
        success_percentage = round(success_percentage, 1)
        error_percentage = round(error_percentage, 1)
        
        # Préparer les données pour le graphique circulaire
        data = [success_percentage, error_percentage]
        labels = ['Total Success Percent', 'Total Error Percent']
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def acceuil_pie_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24 error'  # Vous pouvez utiliser get_latest_sheet(file_path) si nécessaire
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Description', '%']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Extraire les colonnes 'Description' et '%' sous forme de listes
        descriptions = df['Description'].tolist()  # Convertir en liste
        percentages = df['%'].tolist()  # Convertir en liste et s'assurer qu'elles sont des float
        
        # Arrondir les pourcentages au dixième (facultatif)
        percentages = [round(p, 1) for p in percentages]
        
        # Préparer les données pour le graphique circulaire
        response = {
            'data': percentages,
            'labels': descriptions
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def acceuil_area(request):
    try:
        # Chemin vers le fichier Excel
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        # Récupération du nom de la feuille depuis les paramètres GET
        sheet_name = request.GET.get('sheet', 'Aug 24')
        print(f"Feuille sélectionnée : {sheet_name}") # Utiliser 'Aug 24' comme feuille par défaut si aucune n'est spécifiée
        
        # Chargement de la feuille Excel spécifiée
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Date', 'Success % with exclusion']
        for col in required_columns:
            if col not in df.columns:
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par des valeurs par défaut appropriées
        df['Date'] = df['Date'].fillna(method='ffill')  # Remplit les valeurs manquantes avec la dernière valeur connue
        df['Success % with exclusion'] = df['Success % with exclusion'].fillna(0) 
        
        # Conversion de la colonne 'Date' au format de chaîne approprié
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d/%m/%Y')  # Format de date ajusté
        
        # Extraction des données
        labels = df['Date'].tolist()
        line_data = df['Success % with exclusion'].tolist()
        
        response = {
            'labels': labels,
            'line_data': line_data
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def acceuil_bar(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'donnees_produits.xls')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        resultat = df.groupby('Category')['UnitsInStock'].sum()
        
        data = resultat.values.tolist()
        labels = resultat.index.tolist()
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

logger = logging.getLogger(__name__)

def acceuil_bar_line_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name =  'Aug 24 error' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Nombre', '%', 'Description']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Nombre'] = df['Nombre'].fillna(0)
        df['%'] = df['%'].fillna(0)
        df['Description'] = df['Description'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Nombre'].tolist()
        line_data = df['%'].tolist()
        labels = df['Description'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)
    
def acceuil_bar_line(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Total', 'Success % without exclusion', 'Date']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Total'] = df['Total'].fillna(0)
        df['Success % without exclusion'] = df['Success % without exclusion'].fillna(0)
        df['Date'] = df['Date'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Total'].tolist()
        line_data = df['Success % without exclusion'].tolist()
        labels = df['Date'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)

def charts(request):
    return render(request, 'dashboard/page/charts.html')

def tables(request):
    return render(request, 'dashboard/page/tables.html')

def error(request):
    return render(request, 'dashboard/page/404.html')

def blank(request):
    return render(request, 'dashboard/page/blank.html')

#DMC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
def dmc_datatable(request):
    file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')

    # Récupérer la dernière feuille ajoutée
    sheet_name = get_latest_sheet(file_path)

    # Récupérer la feuille précédente
    previous_sheet_name = get_previous_sheet(file_path, sheet_name)

    # Lire les données de la dernière feuille ajoutée
    df_normal = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=0)

    # Lire les données de la feuille précédente (s'il y en a une)
    if previous_sheet_name:
        df_error = pd.read_excel(file_path, sheet_name=previous_sheet_name, skiprows=0)
    else:
        df_error = pd.DataFrame()  # Crée un DataFrame vide si aucune feuille précédente n'existe

    # Traiter les colonnes datetime pour les deux DataFrames
    for df in [df_normal, df_error]:
        date_columns = df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        df.fillna({col: pd.Timestamp.now() for col in date_columns}, inplace=True)

    # Convertir les DataFrames en dictionnaires
    data_normal = df_normal.to_dict(orient='records')
    headers_normal = list(df_normal.columns)
    data_error = df_error.to_dict(orient='records')
    headers_error = list(df_error.columns)

    # Passer les deux ensembles de données au template
    context = {
        'data_normal': data_normal,
        'headers_normal': headers_normal,
        'data_error': data_error,
        'headers_error': headers_error,
    }

    return render(request, 'dashboard/page/application/invigo/dmc.html', context)

def dmc_pie(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Success_A2P', 'Error_A2P', 'Total']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Calculer les valeurs totales
        success_total = df['Success_A2P'].sum()
        error_total = df['Error_A2P'].sum()
        grand_total = df['Total'].sum()

        # Calculer les pourcentages
        success_percentage = (success_total / grand_total) * 100 if grand_total else 0
        error_percentage = (error_total / grand_total) * 100 if grand_total else 0
        # Le reste est la différence jusqu'à 100%
        # remaining_percentage = 100 - success_percentage - error_percentage
        
        # Arrondir les pourcentages au dixième
        success_percentage = round(success_percentage, 1)
        error_percentage = round(error_percentage, 1)
        
        # Préparer les données pour le graphique circulaire
        data = [success_percentage, error_percentage]
        labels = ['Total Success Percent', 'Total Error Percent']
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def dmc_pie_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24 error'  # Vous pouvez utiliser get_latest_sheet(file_path) si nécessaire
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Description', '%']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Extraire les colonnes 'Description' et '%' sous forme de listes
        descriptions = df['Description'].tolist()  # Convertir en liste
        percentages = df['%'].tolist()  # Convertir en liste et s'assurer qu'elles sont des float
        
        # Arrondir les pourcentages au dixième (facultatif)
        percentages = [round(p, 1) for p in percentages]
        
        # Préparer les données pour le graphique circulaire
        response = {
            'data': percentages,
            'labels': descriptions
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def dmc_area(request):
    try:
        # Chemin vers le fichier Excel
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        # Récupération du nom de la feuille depuis les paramètres GET
        sheet_name = request.GET.get('sheet', 'Aug 24')
        print(f"Feuille sélectionnée : {sheet_name}") # Utiliser 'Aug 24' comme feuille par défaut si aucune n'est spécifiée
        
        # Chargement de la feuille Excel spécifiée
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Date', 'Success % with exclusion']
        for col in required_columns:
            if col not in df.columns:
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par des valeurs par défaut appropriées
        df['Date'] = df['Date'].fillna(method='ffill')  # Remplit les valeurs manquantes avec la dernière valeur connue
        df['Success % with exclusion'] = df['Success % with exclusion'].fillna(0) 
        
        # Conversion de la colonne 'Date' au format de chaîne approprié
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d/%m/%Y')  # Format de date ajusté
        
        # Extraction des données
        labels = df['Date'].tolist()
        line_data = df['Success % with exclusion'].tolist()
        
        response = {
            'labels': labels,
            'line_data': line_data
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def dmc_bar(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'donnees_produits.xls')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        resultat = df.groupby('Category')['UnitsInStock'].sum()
        
        data = resultat.values.tolist()
        labels = resultat.index.tolist()
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

logger = logging.getLogger(__name__)

def dmc_bar_line_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name =  'Aug 24 error' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Nombre', '%', 'Description']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Nombre'] = df['Nombre'].fillna(0)
        df['%'] = df['%'].fillna(0)
        df['Description'] = df['Description'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Nombre'].tolist()
        line_data = df['%'].tolist()
        labels = df['Description'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)
    
def dmc_bar_line(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Total', 'Success % without exclusion', 'Date']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Total'] = df['Total'].fillna(0)
        df['Success % without exclusion'] = df['Success % without exclusion'].fillna(0)
        df['Date'] = df['Date'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Total'].tolist()
        line_data = df['Success % without exclusion'].tolist()
        labels = df['Date'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)

#EIR
def eir_datatable(request):
    file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')

    # Récupérer la dernière feuille ajoutée
    sheet_name = get_latest_sheet(file_path)

    # Récupérer la feuille précédente
    previous_sheet_name = get_previous_sheet(file_path, sheet_name)

    # Lire les données de la dernière feuille ajoutée
    df_normal = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=0)

    # Lire les données de la feuille précédente (s'il y en a une)
    if previous_sheet_name:
        df_error = pd.read_excel(file_path, sheet_name=previous_sheet_name, skiprows=0)
    else:
        df_error = pd.DataFrame()  # Crée un DataFrame vide si aucune feuille précédente n'existe

    # Traiter les colonnes datetime pour les deux DataFrames
    for df in [df_normal, df_error]:
        date_columns = df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        df.fillna({col: pd.Timestamp.now() for col in date_columns}, inplace=True)

    # Convertir les DataFrames en dictionnaires
    data_normal = df_normal.to_dict(orient='records')
    headers_normal = list(df_normal.columns)
    data_error = df_error.to_dict(orient='records')
    headers_error = list(df_error.columns)

    # Passer les deux ensembles de données au template
    context = {
        'data_normal': data_normal,
        'headers_normal': headers_normal,
        'data_error': data_error,
        'headers_error': headers_error,
    }

    return render(request, 'dashboard/page/application/invigo/eir.html', context)

def eir_pie(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Success_A2P', 'Error_A2P', 'Total']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Calculer les valeurs totales
        success_total = df['Success_A2P'].sum()
        error_total = df['Error_A2P'].sum()
        grand_total = df['Total'].sum()

        # Calculer les pourcentages
        success_percentage = (success_total / grand_total) * 100 if grand_total else 0
        error_percentage = (error_total / grand_total) * 100 if grand_total else 0
        # Le reste est la différence jusqu'à 100%
        # remaining_percentage = 100 - success_percentage - error_percentage
        
        # Arrondir les pourcentages au dixième
        success_percentage = round(success_percentage, 1)
        error_percentage = round(error_percentage, 1)
        
        # Préparer les données pour le graphique circulaire
        data = [success_percentage, error_percentage]
        labels = ['Total Success Percent', 'Total Error Percent']
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def eir_pie_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24 error'  # Vous pouvez utiliser get_latest_sheet(file_path) si nécessaire
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Description', '%']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Extraire les colonnes 'Description' et '%' sous forme de listes
        descriptions = df['Description'].tolist()  # Convertir en liste
        percentages = df['%'].tolist()  # Convertir en liste et s'assurer qu'elles sont des float
        
        # Arrondir les pourcentages au dixième (facultatif)
        percentages = [round(p, 1) for p in percentages]
        
        # Préparer les données pour le graphique circulaire
        response = {
            'data': percentages,
            'labels': descriptions
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def eir_area(request):
    try:
        # Chemin vers le fichier Excel
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        # Récupération du nom de la feuille depuis les paramètres GET
        sheet_name = request.GET.get('sheet', 'Aug 24')
        print(f"Feuille sélectionnée : {sheet_name}") # Utiliser 'Aug 24' comme feuille par défaut si aucune n'est spécifiée
        
        # Chargement de la feuille Excel spécifiée
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Date', 'Success % with exclusion']
        for col in required_columns:
            if col not in df.columns:
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par des valeurs par défaut appropriées
        df['Date'] = df['Date'].fillna(method='ffill')  # Remplit les valeurs manquantes avec la dernière valeur connue
        df['Success % with exclusion'] = df['Success % with exclusion'].fillna(0) 
        
        # Conversion de la colonne 'Date' au format de chaîne approprié
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d/%m/%Y')  # Format de date ajusté
        
        # Extraction des données
        labels = df['Date'].tolist()
        line_data = df['Success % with exclusion'].tolist()
        
        response = {
            'labels': labels,
            'line_data': line_data
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def eir_bar(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'donnees_produits.xls')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        resultat = df.groupby('Category')['UnitsInStock'].sum()
        
        data = resultat.values.tolist()
        labels = resultat.index.tolist()
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

logger = logging.getLogger(__name__)

def eir_bar_line_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name =  'Aug 24 error' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Nombre', '%', 'Description']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Nombre'] = df['Nombre'].fillna(0)
        df['%'] = df['%'].fillna(0)
        df['Description'] = df['Description'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Nombre'].tolist()
        line_data = df['%'].tolist()
        labels = df['Description'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)
    
def eir_bar_line(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Total', 'Success % without exclusion', 'Date']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Total'] = df['Total'].fillna(0)
        df['Success % without exclusion'] = df['Success % without exclusion'].fillna(0)
        df['Date'] = df['Date'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Total'].tolist()
        line_data = df['Success % without exclusion'].tolist()
        labels = df['Date'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)

#VMS
def vms_datatable(request):
    file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')

    # Récupérer la dernière feuille ajoutée
    sheet_name = get_latest_sheet(file_path)

    # Récupérer la feuille précédente
    previous_sheet_name = get_previous_sheet(file_path, sheet_name)

    # Lire les données de la dernière feuille ajoutée
    df_normal = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=0)

    # Lire les données de la feuille précédente (s'il y en a une)
    if previous_sheet_name:
        df_error = pd.read_excel(file_path, sheet_name=previous_sheet_name, skiprows=0)
    else:
        df_error = pd.DataFrame()  # Crée un DataFrame vide si aucune feuille précédente n'existe

    # Traiter les colonnes datetime pour les deux DataFrames
    for df in [df_normal, df_error]:
        date_columns = df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        df.fillna({col: pd.Timestamp.now() for col in date_columns}, inplace=True)

    # Convertir les DataFrames en dictionnaires
    data_normal = df_normal.to_dict(orient='records')
    headers_normal = list(df_normal.columns)
    data_error = df_error.to_dict(orient='records')
    headers_error = list(df_error.columns)

    # Passer les deux ensembles de données au template
    context = {
        'data_normal': data_normal,
        'headers_normal': headers_normal,
        'data_error': data_error,
        'headers_error': headers_error,
    }

    return render(request, 'dashboard/page/application/appliman/vms.html', context)

def vms_pie(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Success_A2P', 'Error_A2P', 'Total']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Calculer les valeurs totales
        success_total = df['Success_A2P'].sum()
        error_total = df['Error_A2P'].sum()
        grand_total = df['Total'].sum()

        # Calculer les pourcentages
        success_percentage = (success_total / grand_total) * 100 if grand_total else 0
        error_percentage = (error_total / grand_total) * 100 if grand_total else 0
        # Le reste est la différence jusqu'à 100%
        # remaining_percentage = 100 - success_percentage - error_percentage
        
        # Arrondir les pourcentages au dixième
        success_percentage = round(success_percentage, 1)
        error_percentage = round(error_percentage, 1)
        
        # Préparer les données pour le graphique circulaire
        data = [success_percentage, error_percentage]
        labels = ['Total Success Percent', 'Total Error Percent']
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def vms_pie_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24 error'  # Vous pouvez utiliser get_latest_sheet(file_path) si nécessaire
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Description', '%']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Extraire les colonnes 'Description' et '%' sous forme de listes
        descriptions = df['Description'].tolist()  # Convertir en liste
        percentages = df['%'].tolist()  # Convertir en liste et s'assurer qu'elles sont des float
        
        # Arrondir les pourcentages au dixième (facultatif)
        percentages = [round(p, 1) for p in percentages]
        
        # Préparer les données pour le graphique circulaire
        response = {
            'data': percentages,
            'labels': descriptions
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def vms_area(request):
    try:
        # Chemin vers le fichier Excel
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        # Récupération du nom de la feuille depuis les paramètres GET
        sheet_name = request.GET.get('sheet', 'Aug 24')
        print(f"Feuille sélectionnée : {sheet_name}") # Utiliser 'Aug 24' comme feuille par défaut si aucune n'est spécifiée
        
        # Chargement de la feuille Excel spécifiée
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Date', 'Success % with exclusion']
        for col in required_columns:
            if col not in df.columns:
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par des valeurs par défaut appropriées
        df['Date'] = df['Date'].fillna(method='ffill')  # Remplit les valeurs manquantes avec la dernière valeur connue
        df['Success % with exclusion'] = df['Success % with exclusion'].fillna(0) 
        
        # Conversion de la colonne 'Date' au format de chaîne approprié
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d/%m/%Y')  # Format de date ajusté
        
        # Extraction des données
        labels = df['Date'].tolist()
        line_data = df['Success % with exclusion'].tolist()
        
        response = {
            'labels': labels,
            'line_data': line_data
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def vms_bar(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'donnees_produits.xls')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        resultat = df.groupby('Category')['UnitsInStock'].sum()
        
        data = resultat.values.tolist()
        labels = resultat.index.tolist()
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

logger = logging.getLogger(__name__)

def vms_bar_line_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name =  'Aug 24 error' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Nombre', '%', 'Description']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Nombre'] = df['Nombre'].fillna(0)
        df['%'] = df['%'].fillna(0)
        df['Description'] = df['Description'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Nombre'].tolist()
        line_data = df['%'].tolist()
        labels = df['Description'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)
    
def vms_bar_line(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Total', 'Success % without exclusion', 'Date']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Total'] = df['Total'].fillna(0)
        df['Success % without exclusion'] = df['Success % without exclusion'].fillna(0)
        df['Date'] = df['Date'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Total'].tolist()
        line_data = df['Success % without exclusion'].tolist()
        labels = df['Date'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)

#MCN
def mcn_datatable(request):
    file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')

    # Récupérer la dernière feuille ajoutée
    sheet_name = get_latest_sheet(file_path)

    # Récupérer la feuille précédente
    previous_sheet_name = get_previous_sheet(file_path, sheet_name)

    # Lire les données de la dernière feuille ajoutée
    df_normal = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=0)

    # Lire les données de la feuille précédente (s'il y en a une)
    if previous_sheet_name:
        df_error = pd.read_excel(file_path, sheet_name=previous_sheet_name, skiprows=0)
    else:
        df_error = pd.DataFrame()  # Crée un DataFrame vide si aucune feuille précédente n'existe

    # Traiter les colonnes datetime pour les deux DataFrames
    for df in [df_normal, df_error]:
        date_columns = df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        df.fillna({col: pd.Timestamp.now() for col in date_columns}, inplace=True)

    # Convertir les DataFrames en dictionnaires
    data_normal = df_normal.to_dict(orient='records')
    headers_normal = list(df_normal.columns)
    data_error = df_error.to_dict(orient='records')
    headers_error = list(df_error.columns)

    # Passer les deux ensembles de données au template
    context = {
        'data_normal': data_normal,
        'headers_normal': headers_normal,
        'data_error': data_error,
        'headers_error': headers_error,
    }

    return render(request, 'dashboard/page/application/appliman/mcn.html', context)

def mcn_pie(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Success_A2P', 'Error_A2P', 'Total']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Calculer les valeurs totales
        success_total = df['Success_A2P'].sum()
        error_total = df['Error_A2P'].sum()
        grand_total = df['Total'].sum()

        # Calculer les pourcentages
        success_percentage = (success_total / grand_total) * 100 if grand_total else 0
        error_percentage = (error_total / grand_total) * 100 if grand_total else 0
        # Le reste est la différence jusqu'à 100%
        # remaining_percentage = 100 - success_percentage - error_percentage
        
        # Arrondir les pourcentages au dixième
        success_percentage = round(success_percentage, 1)
        error_percentage = round(error_percentage, 1)
        
        # Préparer les données pour le graphique circulaire
        data = [success_percentage, error_percentage]
        labels = ['Total Success Percent', 'Total Error Percent']
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def mcn_pie_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24 error'  # Vous pouvez utiliser get_latest_sheet(file_path) si nécessaire
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Description', '%']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Extraire les colonnes 'Description' et '%' sous forme de listes
        descriptions = df['Description'].tolist()  # Convertir en liste
        percentages = df['%'].tolist()  # Convertir en liste et s'assurer qu'elles sont des float
        
        # Arrondir les pourcentages au dixième (facultatif)
        percentages = [round(p, 1) for p in percentages]
        
        # Préparer les données pour le graphique circulaire
        response = {
            'data': percentages,
            'labels': descriptions
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def mcn_area(request):
    try:
        # Chemin vers le fichier Excel
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        # Récupération du nom de la feuille depuis les paramètres GET
        sheet_name = request.GET.get('sheet', 'Aug 24')
        print(f"Feuille sélectionnée : {sheet_name}") # Utiliser 'Aug 24' comme feuille par défaut si aucune n'est spécifiée
        
        # Chargement de la feuille Excel spécifiée
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Date', 'Success % with exclusion']
        for col in required_columns:
            if col not in df.columns:
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par des valeurs par défaut appropriées
        df['Date'] = df['Date'].fillna(method='ffill')  # Remplit les valeurs manquantes avec la dernière valeur connue
        df['Success % with exclusion'] = df['Success % with exclusion'].fillna(0) 
        
        # Conversion de la colonne 'Date' au format de chaîne approprié
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d/%m/%Y')  # Format de date ajusté
        
        # Extraction des données
        labels = df['Date'].tolist()
        line_data = df['Success % with exclusion'].tolist()
        
        response = {
            'labels': labels,
            'line_data': line_data
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def mcn_bar(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'donnees_produits.xls')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        resultat = df.groupby('Category')['UnitsInStock'].sum()
        
        data = resultat.values.tolist()
        labels = resultat.index.tolist()
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

logger = logging.getLogger(__name__)

def mcn_bar_line_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name =  'Aug 24 error' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Nombre', '%', 'Description']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Nombre'] = df['Nombre'].fillna(0)
        df['%'] = df['%'].fillna(0)
        df['Description'] = df['Description'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Nombre'].tolist()
        line_data = df['%'].tolist()
        labels = df['Description'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)
    
def mcn_bar_line(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Total', 'Success % without exclusion', 'Date']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Total'] = df['Total'].fillna(0)
        df['Success % without exclusion'] = df['Success % without exclusion'].fillna(0)
        df['Date'] = df['Date'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Total'].tolist()
        line_data = df['Success % without exclusion'].tolist()
        labels = df['Date'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)

#IVR
def ivr_datatable(request):
    file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')

    # Récupérer la dernière feuille ajoutée
    sheet_name = get_latest_sheet(file_path)

    # Récupérer la feuille précédente
    previous_sheet_name = get_previous_sheet(file_path, sheet_name)

    # Lire les données de la dernière feuille ajoutée
    df_normal = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=0)

    # Lire les données de la feuille précédente (s'il y en a une)
    if previous_sheet_name:
        df_error = pd.read_excel(file_path, sheet_name=previous_sheet_name, skiprows=0)
    else:
        df_error = pd.DataFrame()  # Crée un DataFrame vide si aucune feuille précédente n'existe

    # Traiter les colonnes datetime pour les deux DataFrames
    for df in [df_normal, df_error]:
        date_columns = df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        df.fillna({col: pd.Timestamp.now() for col in date_columns}, inplace=True)

    # Convertir les DataFrames en dictionnaires
    data_normal = df_normal.to_dict(orient='records')
    headers_normal = list(df_normal.columns)
    data_error = df_error.to_dict(orient='records')
    headers_error = list(df_error.columns)

    # Passer les deux ensembles de données au template
    context = {
        'data_normal': data_normal,
        'headers_normal': headers_normal,
        'data_error': data_error,
        'headers_error': headers_error,
    }

    return render(request, 'dashboard/page/application/appliman/ivr.html', context)

def ivr_pie(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Success_A2P', 'Error_A2P', 'Total']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Calculer les valeurs totales
        success_total = df['Success_A2P'].sum()
        error_total = df['Error_A2P'].sum()
        grand_total = df['Total'].sum()

        # Calculer les pourcentages
        success_percentage = (success_total / grand_total) * 100 if grand_total else 0
        error_percentage = (error_total / grand_total) * 100 if grand_total else 0
        # Le reste est la différence jusqu'à 100%
        # remaining_percentage = 100 - success_percentage - error_percentage
        
        # Arrondir les pourcentages au dixième
        success_percentage = round(success_percentage, 1)
        error_percentage = round(error_percentage, 1)
        
        # Préparer les données pour le graphique circulaire
        data = [success_percentage, error_percentage]
        labels = ['Total Success Percent', 'Total Error Percent']
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def ivr_pie_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24 error'  # Vous pouvez utiliser get_latest_sheet(file_path) si nécessaire
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Description', '%']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Extraire les colonnes 'Description' et '%' sous forme de listes
        descriptions = df['Description'].tolist()  # Convertir en liste
        percentages = df['%'].tolist()  # Convertir en liste et s'assurer qu'elles sont des float
        
        # Arrondir les pourcentages au dixième (facultatif)
        percentages = [round(p, 1) for p in percentages]
        
        # Préparer les données pour le graphique circulaire
        response = {
            'data': percentages,
            'labels': descriptions
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def ivr_area(request):
    try:
        # Chemin vers le fichier Excel
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        # Récupération du nom de la feuille depuis les paramètres GET
        sheet_name = request.GET.get('sheet', 'Aug 24')
        print(f"Feuille sélectionnée : {sheet_name}") # Utiliser 'Aug 24' comme feuille par défaut si aucune n'est spécifiée
        
        # Chargement de la feuille Excel spécifiée
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Date', 'Success % with exclusion']
        for col in required_columns:
            if col not in df.columns:
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par des valeurs par défaut appropriées
        df['Date'] = df['Date'].fillna(method='ffill')  # Remplit les valeurs manquantes avec la dernière valeur connue
        df['Success % with exclusion'] = df['Success % with exclusion'].fillna(0) 
        
        # Conversion de la colonne 'Date' au format de chaîne approprié
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d/%m/%Y')  # Format de date ajusté
        
        # Extraction des données
        labels = df['Date'].tolist()
        line_data = df['Success % with exclusion'].tolist()
        
        response = {
            'labels': labels,
            'line_data': line_data
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def ivr_bar(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'donnees_produits.xls')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        resultat = df.groupby('Category')['UnitsInStock'].sum()
        
        data = resultat.values.tolist()
        labels = resultat.index.tolist()
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

logger = logging.getLogger(__name__)

def ivr_bar_line_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name =  'Aug 24 error' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Nombre', '%', 'Description']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Nombre'] = df['Nombre'].fillna(0)
        df['%'] = df['%'].fillna(0)
        df['Description'] = df['Description'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Nombre'].tolist()
        line_data = df['%'].tolist()
        labels = df['Description'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)
    
def ivr_bar_line(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Total', 'Success % without exclusion', 'Date']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Total'] = df['Total'].fillna(0)
        df['Success % without exclusion'] = df['Success % without exclusion'].fillna(0)
        df['Date'] = df['Date'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Total'].tolist()
        line_data = df['Success % without exclusion'].tolist()
        labels = df['Date'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)

#OBD
def obd_datatable(request):
    file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')

    # Récupérer la dernière feuille ajoutée
    sheet_name = get_latest_sheet(file_path)

    # Récupérer la feuille précédente
    previous_sheet_name = get_previous_sheet(file_path, sheet_name)

    # Lire les données de la dernière feuille ajoutée
    df_normal = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=0)

    # Lire les données de la feuille précédente (s'il y en a une)
    if previous_sheet_name:
        df_error = pd.read_excel(file_path, sheet_name=previous_sheet_name, skiprows=0)
    else:
        df_error = pd.DataFrame()  # Crée un DataFrame vide si aucune feuille précédente n'existe

    # Traiter les colonnes datetime pour les deux DataFrames
    for df in [df_normal, df_error]:
        date_columns = df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        df.fillna({col: pd.Timestamp.now() for col in date_columns}, inplace=True)

    # Convertir les DataFrames en dictionnaires
    data_normal = df_normal.to_dict(orient='records')
    headers_normal = list(df_normal.columns)
    data_error = df_error.to_dict(orient='records')
    headers_error = list(df_error.columns)

    # Passer les deux ensembles de données au template
    context = {
        'data_normal': data_normal,
        'headers_normal': headers_normal,
        'data_error': data_error,
        'headers_error': headers_error,
    }

    return render(request, 'dashboard/page/application/appliman/obd.html', context)

def obd_pie(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Success_A2P', 'Error_A2P', 'Total']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Calculer les valeurs totales
        success_total = df['Success_A2P'].sum()
        error_total = df['Error_A2P'].sum()
        grand_total = df['Total'].sum()

        # Calculer les pourcentages
        success_percentage = (success_total / grand_total) * 100 if grand_total else 0
        error_percentage = (error_total / grand_total) * 100 if grand_total else 0
        # Le reste est la différence jusqu'à 100%
        # remaining_percentage = 100 - success_percentage - error_percentage
        
        # Arrondir les pourcentages au dixième
        success_percentage = round(success_percentage, 1)
        error_percentage = round(error_percentage, 1)
        
        # Préparer les données pour le graphique circulaire
        data = [success_percentage, error_percentage]
        labels = ['Total Success Percent', 'Total Error Percent']
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def obd_pie_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24 error'  # Vous pouvez utiliser get_latest_sheet(file_path) si nécessaire
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Description', '%']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Extraire les colonnes 'Description' et '%' sous forme de listes
        descriptions = df['Description'].tolist()  # Convertir en liste
        percentages = df['%'].tolist()  # Convertir en liste et s'assurer qu'elles sont des float
        
        # Arrondir les pourcentages au dixième (facultatif)
        percentages = [round(p, 1) for p in percentages]
        
        # Préparer les données pour le graphique circulaire
        response = {
            'data': percentages,
            'labels': descriptions
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def obd_area(request):
    try:
        # Chemin vers le fichier Excel
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        # Récupération du nom de la feuille depuis les paramètres GET
        sheet_name = request.GET.get('sheet', 'Aug 24')
        print(f"Feuille sélectionnée : {sheet_name}") # Utiliser 'Aug 24' comme feuille par défaut si aucune n'est spécifiée
        
        # Chargement de la feuille Excel spécifiée
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Date', 'Success % with exclusion']
        for col in required_columns:
            if col not in df.columns:
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par des valeurs par défaut appropriées
        df['Date'] = df['Date'].fillna(method='ffill')  # Remplit les valeurs manquantes avec la dernière valeur connue
        df['Success % with exclusion'] = df['Success % with exclusion'].fillna(0) 
        
        # Conversion de la colonne 'Date' au format de chaîne approprié
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d/%m/%Y')  # Format de date ajusté
        
        # Extraction des données
        labels = df['Date'].tolist()
        line_data = df['Success % with exclusion'].tolist()
        
        response = {
            'labels': labels,
            'line_data': line_data
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def obd_bar(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'donnees_produits.xls')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        resultat = df.groupby('Category')['UnitsInStock'].sum()
        
        data = resultat.values.tolist()
        labels = resultat.index.tolist()
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

logger = logging.getLogger(__name__)

def obd_bar_line_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name =  'Aug 24 error' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Nombre', '%', 'Description']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Nombre'] = df['Nombre'].fillna(0)
        df['%'] = df['%'].fillna(0)
        df['Description'] = df['Description'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Nombre'].tolist()
        line_data = df['%'].tolist()
        labels = df['Description'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)
    
def obd_bar_line(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Total', 'Success % without exclusion', 'Date']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Total'] = df['Total'].fillna(0)
        df['Success % without exclusion'] = df['Success % without exclusion'].fillna(0)
        df['Date'] = df['Date'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Total'].tolist()
        line_data = df['Success % without exclusion'].tolist()
        labels = df['Date'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)

#Collect Call
def collect_call_datatable(request):
    file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')

    # Récupérer la dernière feuille ajoutée
    sheet_name = get_latest_sheet(file_path)

    # Récupérer la feuille précédente
    previous_sheet_name = get_previous_sheet(file_path, sheet_name)

    # Lire les données de la dernière feuille ajoutée
    df_normal = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=0)

    # Lire les données de la feuille précédente (s'il y en a une)
    if previous_sheet_name:
        df_error = pd.read_excel(file_path, sheet_name=previous_sheet_name, skiprows=0)
    else:
        df_error = pd.DataFrame()  # Crée un DataFrame vide si aucune feuille précédente n'existe

    # Traiter les colonnes datetime pour les deux DataFrames
    for df in [df_normal, df_error]:
        date_columns = df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        df.fillna({col: pd.Timestamp.now() for col in date_columns}, inplace=True)

    # Convertir les DataFrames en dictionnaires
    data_normal = df_normal.to_dict(orient='records')
    headers_normal = list(df_normal.columns)
    data_error = df_error.to_dict(orient='records')
    headers_error = list(df_error.columns)

    # Passer les deux ensembles de données au template
    context = {
        'data_normal': data_normal,
        'headers_normal': headers_normal,
        'data_error': data_error,
        'headers_error': headers_error,
    }

    return render(request, 'dashboard/page/application/appliman/collect_call.html', context)

def collect_call_pie(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Success_A2P', 'Error_A2P', 'Total']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Calculer les valeurs totales
        success_total = df['Success_A2P'].sum()
        error_total = df['Error_A2P'].sum()
        grand_total = df['Total'].sum()

        # Calculer les pourcentages
        success_percentage = (success_total / grand_total) * 100 if grand_total else 0
        error_percentage = (error_total / grand_total) * 100 if grand_total else 0
        # Le reste est la différence jusqu'à 100%
        # remaining_percentage = 100 - success_percentage - error_percentage
        
        # Arrondir les pourcentages au dixième
        success_percentage = round(success_percentage, 1)
        error_percentage = round(error_percentage, 1)
        
        # Préparer les données pour le graphique circulaire
        data = [success_percentage, error_percentage]
        labels = ['Total Success Percent', 'Total Error Percent']
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def collect_call_pie_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24 error'  # Vous pouvez utiliser get_latest_sheet(file_path) si nécessaire
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Description', '%']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Extraire les colonnes 'Description' et '%' sous forme de listes
        descriptions = df['Description'].tolist()  # Convertir en liste
        percentages = df['%'].tolist()  # Convertir en liste et s'assurer qu'elles sont des float
        
        # Arrondir les pourcentages au dixième (facultatif)
        percentages = [round(p, 1) for p in percentages]
        
        # Préparer les données pour le graphique circulaire
        response = {
            'data': percentages,
            'labels': descriptions
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def collect_call_area(request):
    try:
        # Chemin vers le fichier Excel
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        # Récupération du nom de la feuille depuis les paramètres GET
        sheet_name = request.GET.get('sheet', 'Aug 24')
        print(f"Feuille sélectionnée : {sheet_name}") # Utiliser 'Aug 24' comme feuille par défaut si aucune n'est spécifiée
        
        # Chargement de la feuille Excel spécifiée
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Date', 'Success % with exclusion']
        for col in required_columns:
            if col not in df.columns:
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par des valeurs par défaut appropriées
        df['Date'] = df['Date'].fillna(method='ffill')  # Remplit les valeurs manquantes avec la dernière valeur connue
        df['Success % with exclusion'] = df['Success % with exclusion'].fillna(0) 
        
        # Conversion de la colonne 'Date' au format de chaîne approprié
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d/%m/%Y')  # Format de date ajusté
        
        # Extraction des données
        labels = df['Date'].tolist()
        line_data = df['Success % with exclusion'].tolist()
        
        response = {
            'labels': labels,
            'line_data': line_data
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def collect_call_bar(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'donnees_produits.xls')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        resultat = df.groupby('Category')['UnitsInStock'].sum()
        
        data = resultat.values.tolist()
        labels = resultat.index.tolist()
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

logger = logging.getLogger(__name__)

def collect_call_bar_line_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name =  'Aug 24 error' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Nombre', '%', 'Description']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Nombre'] = df['Nombre'].fillna(0)
        df['%'] = df['%'].fillna(0)
        df['Description'] = df['Description'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Nombre'].tolist()
        line_data = df['%'].tolist()
        labels = df['Description'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)
    
def collect_call_bar_line(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Total', 'Success % without exclusion', 'Date']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Total'] = df['Total'].fillna(0)
        df['Success % without exclusion'] = df['Success % without exclusion'].fillna(0)
        df['Date'] = df['Date'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Total'].tolist()
        line_data = df['Success % without exclusion'].tolist()
        labels = df['Date'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)

#Autocall Completion
def autocall_completion_datatable(request):
    file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')

    # Récupérer la dernière feuille ajoutée
    sheet_name = get_latest_sheet(file_path)

    # Récupérer la feuille précédente
    previous_sheet_name = get_previous_sheet(file_path, sheet_name)

    # Lire les données de la dernière feuille ajoutée
    df_normal = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=0)

    # Lire les données de la feuille précédente (s'il y en a une)
    if previous_sheet_name:
        df_error = pd.read_excel(file_path, sheet_name=previous_sheet_name, skiprows=0)
    else:
        df_error = pd.DataFrame()  # Crée un DataFrame vide si aucune feuille précédente n'existe

    # Traiter les colonnes datetime pour les deux DataFrames
    for df in [df_normal, df_error]:
        date_columns = df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        df.fillna({col: pd.Timestamp.now() for col in date_columns}, inplace=True)

    # Convertir les DataFrames en dictionnaires
    data_normal = df_normal.to_dict(orient='records')
    headers_normal = list(df_normal.columns)
    data_error = df_error.to_dict(orient='records')
    headers_error = list(df_error.columns)

    # Passer les deux ensembles de données au template
    context = {
        'data_normal': data_normal,
        'headers_normal': headers_normal,
        'data_error': data_error,
        'headers_error': headers_error,
    }

    return render(request, 'dashboard/page/application/appliman/autocall_completion.html', context)

def autocall_completion_pie(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Success_A2P', 'Error_A2P', 'Total']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Calculer les valeurs totales
        success_total = df['Success_A2P'].sum()
        error_total = df['Error_A2P'].sum()
        grand_total = df['Total'].sum()

        # Calculer les pourcentages
        success_percentage = (success_total / grand_total) * 100 if grand_total else 0
        error_percentage = (error_total / grand_total) * 100 if grand_total else 0
        # Le reste est la différence jusqu'à 100%
        # remaining_percentage = 100 - success_percentage - error_percentage
        
        # Arrondir les pourcentages au dixième
        success_percentage = round(success_percentage, 1)
        error_percentage = round(error_percentage, 1)
        
        # Préparer les données pour le graphique circulaire
        data = [success_percentage, error_percentage]
        labels = ['Total Success Percent', 'Total Error Percent']
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def autocall_completion_pie_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24 error'  # Vous pouvez utiliser get_latest_sheet(file_path) si nécessaire
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Description', '%']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Extraire les colonnes 'Description' et '%' sous forme de listes
        descriptions = df['Description'].tolist()  # Convertir en liste
        percentages = df['%'].tolist()  # Convertir en liste et s'assurer qu'elles sont des float
        
        # Arrondir les pourcentages au dixième (facultatif)
        percentages = [round(p, 1) for p in percentages]
        
        # Préparer les données pour le graphique circulaire
        response = {
            'data': percentages,
            'labels': descriptions
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def autocall_completion_area(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24'  # Assurez-vous que ce nom de feuille est correct
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Date', 'Success % with exclusion']
        for col in required_columns:
            if col not in df.columns:
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par des valeurs par défaut appropriées
        df['Date'] = df['Date'].fillna(method='ffill')  # Remplit les valeurs manquantes avec la dernière valeur connue
        df['Success % with exclusion'] = df['Success % with exclusion'].fillna(0) 
        
        # Conversion de la colonne 'Date' au format de chaîne approprié
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d/%m/%Y')  # Format de date ajusté
        
        # Extraction des données
        labels = df['Date'].tolist()
        line_data = df['Success % with exclusion'].tolist()
        
        response = {
            'labels': labels,
            'line_data': line_data
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def autocall_completion_bar(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'donnees_produits.xls')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        resultat = df.groupby('Category')['UnitsInStock'].sum()
        
        data = resultat.values.tolist()
        labels = resultat.index.tolist()
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

logger = logging.getLogger(__name__)

def autocall_completion_bar_line_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name =  'Aug 24 error' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Nombre', '%', 'Description']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Nombre'] = df['Nombre'].fillna(0)
        df['%'] = df['%'].fillna(0)
        df['Description'] = df['Description'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Nombre'].tolist()
        line_data = df['%'].tolist()
        labels = df['Description'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)
    
def autocall_completion_bar_line(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Total', 'Success % without exclusion', 'Date']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Total'] = df['Total'].fillna(0)
        df['Success % without exclusion'] = df['Success % without exclusion'].fillna(0)
        df['Date'] = df['Date'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Total'].tolist()
        line_data = df['Success % without exclusion'].tolist()
        labels = df['Date'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)

#CRBT
def crbt_datatable(request):
    file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')

    # Récupérer la dernière feuille ajoutée
    sheet_name = get_latest_sheet(file_path)

    # Récupérer la feuille précédente
    previous_sheet_name = get_previous_sheet(file_path, sheet_name)

    # Lire les données de la dernière feuille ajoutée
    df_normal = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=0)

    # Lire les données de la feuille précédente (s'il y en a une)
    if previous_sheet_name:
        df_error = pd.read_excel(file_path, sheet_name=previous_sheet_name, skiprows=0)
    else:
        df_error = pd.DataFrame()  # Crée un DataFrame vide si aucune feuille précédente n'existe

    # Traiter les colonnes datetime pour les deux DataFrames
    for df in [df_normal, df_error]:
        date_columns = df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        df.fillna({col: pd.Timestamp.now() for col in date_columns}, inplace=True)

    # Convertir les DataFrames en dictionnaires
    data_normal = df_normal.to_dict(orient='records')
    headers_normal = list(df_normal.columns)
    data_error = df_error.to_dict(orient='records')
    headers_error = list(df_error.columns)

    # Passer les deux ensembles de données au template
    context = {
        'data_normal': data_normal,
        'headers_normal': headers_normal,
        'data_error': data_error,
        'headers_error': headers_error,
    }

    return render(request, 'dashboard/page/application/6d/crbt.html', context)

def crbt_pie(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Success_A2P', 'Error_A2P', 'Total']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Calculer les valeurs totales
        success_total = df['Success_A2P'].sum()
        error_total = df['Error_A2P'].sum()
        grand_total = df['Total'].sum()

        # Calculer les pourcentages
        success_percentage = (success_total / grand_total) * 100 if grand_total else 0
        error_percentage = (error_total / grand_total) * 100 if grand_total else 0
        # Le reste est la différence jusqu'à 100%
        # remaining_percentage = 100 - success_percentage - error_percentage
        
        # Arrondir les pourcentages au dixième
        success_percentage = round(success_percentage, 1)
        error_percentage = round(error_percentage, 1)
        
        # Préparer les données pour le graphique circulaire
        data = [success_percentage, error_percentage]
        labels = ['Total Success Percent', 'Total Error Percent']
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def crbt_pie_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24 error'  # Vous pouvez utiliser get_latest_sheet(file_path) si nécessaire
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Description', '%']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Extraire les colonnes 'Description' et '%' sous forme de listes
        descriptions = df['Description'].tolist()  # Convertir en liste
        percentages = df['%'].tolist()  # Convertir en liste et s'assurer qu'elles sont des float
        
        # Arrondir les pourcentages au dixième (facultatif)
        percentages = [round(p, 1) for p in percentages]
        
        # Préparer les données pour le graphique circulaire
        response = {
            'data': percentages,
            'labels': descriptions
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def crbt_area(request):
    try:
        # Chemin vers le fichier Excel
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        # Récupération du nom de la feuille depuis les paramètres GET
        sheet_name = request.GET.get('sheet', 'Aug 24')
        print(f"Feuille sélectionnée : {sheet_name}") # Utiliser 'Aug 24' comme feuille par défaut si aucune n'est spécifiée
        
        # Chargement de la feuille Excel spécifiée
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Date', 'Success % with exclusion']
        for col in required_columns:
            if col not in df.columns:
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par des valeurs par défaut appropriées
        df['Date'] = df['Date'].fillna(method='ffill')  # Remplit les valeurs manquantes avec la dernière valeur connue
        df['Success % with exclusion'] = df['Success % with exclusion'].fillna(0) 
        
        # Conversion de la colonne 'Date' au format de chaîne approprié
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d/%m/%Y')  # Format de date ajusté
        
        # Extraction des données
        labels = df['Date'].tolist()
        line_data = df['Success % with exclusion'].tolist()
        
        response = {
            'labels': labels,
            'line_data': line_data
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def crbt_bar(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'donnees_produits.xls')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        resultat = df.groupby('Category')['UnitsInStock'].sum()
        
        data = resultat.values.tolist()
        labels = resultat.index.tolist()
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

logger = logging.getLogger(__name__)

def crbt_bar_line_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name =  'Aug 24 error' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Nombre', '%', 'Description']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Nombre'] = df['Nombre'].fillna(0)
        df['%'] = df['%'].fillna(0)
        df['Description'] = df['Description'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Nombre'].tolist()
        line_data = df['%'].tolist()
        labels = df['Description'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)
    
def crbt_bar_line(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Total', 'Success % without exclusion', 'Date']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Total'] = df['Total'].fillna(0)
        df['Success % without exclusion'] = df['Success % without exclusion'].fillna(0)
        df['Date'] = df['Date'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Total'].tolist()
        line_data = df['Success % without exclusion'].tolist()
        labels = df['Date'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)

#SMS PRO
def sms_pro_view1(request):
    file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'donnees_normales.xlsx')

    try:
        # Lire les données de l'Excel
        df = pd.read_excel(file_path)
        
        # Remplir les valeurs manquantes
        df.fillna('', inplace=True)
        
        # Convertir les DataFrames en dictionnaires
        data_normal = df.to_dict(orient='records')
        headers_normal = list(df.columns)

        context = {
            'data_normal': data_normal,
            'headers_normal': headers_normal,
        }
        print(headers_normal)

        return render(request, 'dashboard/page/application/powerme_mobile/sms_pro.html', context)

    except Exception as e:
        return render(request, 'dashboard/page/application/powerme_mobile/sms_pro.html', {
            'error_message': f"Erreur lors de la lecture du fichier Excel : {e}"
        })

# def sms_pro_view2(request):
#     file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')

#     # Récupérer la dernière feuille ajoutée
#     sheet_name = get_latest_sheet(file_path)

#     # Récupérer la feuille précédente
#     previous_sheet_name = get_previous_sheet(file_path, sheet_name)

#     # Lire les données de la dernière feuille ajoutée
#     df_normal = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=0)

#     # Lire les données de la feuille précédente (s'il y en a une)
#     if previous_sheet_name:
#         df_error = pd.read_excel(file_path, sheet_name=previous_sheet_name, skiprows=0)
#     else:
#         df_error = pd.DataFrame()  # Crée un DataFrame vide si aucune feuille précédente n'existe

#     # Traiter les colonnes datetime pour les deux DataFrames
#     for df in [df_normal, df_error]:
#         date_columns = df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns
#         for col in date_columns:
#             df[col] = pd.to_datetime(df[col], errors='coerce')
#         df.fillna({col: pd.Timestamp.now() for col in date_columns}, inplace=True)

#     # Convertir les DataFrames en dictionnaires
#     data_normal = df_normal.to_dict(orient='records')
#     headers_normal = list(df_normal.columns)
#     data_error = df_error.to_dict(orient='records')
#     headers_error = list(df_error.columns)

#     # Passer les deux ensembles de données au template
#     context = {
#         'data_normal': data_normal,
#         'headers_normal': headers_normal,
#         'data_error': data_error,
#         'headers_error': headers_error,
#     }

#     return render(request, 'dashboard/page/application/6d/crbt.html', context)

# def sms_pro_datatable(request):
#     # Chemin vers le fichier Excel
#     file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')

#     # Vérification de l'existence du fichier
#     if not os.path.exists(file_path):
#         return JsonResponse({'error': 'Le fichier Excel est introuvable.'}, status=404)

#     try:
#         # Lire les données de la feuille Excel
#         df = pd.read_excel(file_path)

#         # Traiter les colonnes datetime
#         date_columns = df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns
#         for col in date_columns:
#             df[col] = pd.to_datetime(df[col], errors='coerce')
#             df[col].fillna(pd.Timestamp.now(), inplace=True)

#         # Appliquer le forward fill pour remplir les valeurs manquantes dans les colonnes datetime
#         for col in date_columns:
#             df[col] = df[col].fillna(method='ffill')

#         # Remplir toutes les colonnes vides
#         df.fillna({
#             col: '' if df[col].dtype == 'object' else 0 for col in df.columns
#         }, inplace=True)

#         # Convertir le DataFrame en dictionnaire (liste de dictionnaires)
#         data_normal = df.to_dict(orient='records')

#         # Retourner les données au format JSON
#         return JsonResponse({'data': data_normal}, safe=False)

#     except Exception as e:
#         return JsonResponse({'error': f"Erreur lors de la lecture du fichier Excel : {e}"}, status=500)

def sms_pro_pie(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Success_A2P', 'Error_A2P', 'Total']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Calculer les valeurs totales
        success_total = df['Success_A2P'].sum()
        error_total = df['Error_A2P'].sum()
        grand_total = df['Total'].sum()

        # Calculer les pourcentages
        success_percentage = (success_total / grand_total) * 100 if grand_total else 0
        error_percentage = (error_total / grand_total) * 100 if grand_total else 0
        # Le reste est la différence jusqu'à 100%
        # remaining_percentage = 100 - success_percentage - error_percentage
        
        # Arrondir les pourcentages au dixième
        success_percentage = round(success_percentage, 1)
        error_percentage = round(error_percentage, 1)
        
        # Préparer les données pour le graphique circulaire
        data = [success_percentage, error_percentage]
        labels = ['Total Success Percent', 'Total Error Percent']
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def sms_pro_pie_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24 error'  # Vous pouvez utiliser get_latest_sheet(file_path) si nécessaire
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Description', '%']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Extraire les colonnes 'Description' et '%' sous forme de listes
        descriptions = df['Description'].tolist()  # Convertir en liste
        percentages = df['%'].tolist()  # Convertir en liste et s'assurer qu'elles sont des float
        
        # Arrondir les pourcentages au dixième (facultatif)
        percentages = [round(p, 1) for p in percentages]
        
        # Préparer les données pour le graphique circulaire
        response = {
            'data': percentages,
            'labels': descriptions
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def sms_pro_area(request):
    try:
        # Récupérer les paramètres de la requête
        date_debut = request.GET.get('date_debut')
        date_fin = request.GET.get('date_fin')

        # Chemin vers le fichier Excel
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'donnees_normales.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        # Chargement de la feuille Excel spécifiée
        df = pd.read_excel(file_path)
        
        required_columns = ['Date', 'Success % with exclusion']
        for col in required_columns:
            if col not in df.columns:
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Conversion de la colonne 'Date' en datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Filtrer les données si des dates sont fournies
        if date_debut and date_fin:
            date_debut = pd.to_datetime(date_debut)
            date_fin = pd.to_datetime(date_fin)
            df = df[(df['Date'] >= date_debut) & (df['Date'] <= date_fin)]
        
        # Trier les données par date
        df = df.sort_values('Date')
        
        # Conversion de la colonne 'Date' au format de chaîne pour l'affichage
        df['Date'] = df['Date'].dt.strftime('%d/%m/%Y')
        
        # Extraction des données
        labels = df['Date'].tolist()
        line_data = df['Success % with exclusion'].tolist()
        
        response = {
            'labels': labels,
            'line_data': line_data
        }
        
        return JsonResponse(response)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def sms_pro_bar(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'donnees_produits.xls')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        resultat = df.groupby('Category')['UnitsInStock'].sum()
        
        data = resultat.values.tolist()
        labels = resultat.index.tolist()
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

logger = logging.getLogger(__name__)

def sms_Pro_bar_line_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = request.GET.get('sheet', 'Aug 24 error')  # Rendre le nom de la feuille dynamique
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Nombre', '%', 'Description']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante dans la feuille {sheet_name}: {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par des valeurs par défaut
        df['Nombre'] = df['Nombre'].fillna(0)
        df['%'] = df['%'].fillna(0)
        df['Description'] = df['Description'].fillna('Inconnu')  # Valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Nombre'].tolist()
        line_data = df['%'].tolist()
        labels = df['Description'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        logger.info(f"Réponse envoyée pour la feuille {sheet_name}.")
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except KeyError as e:
        logger.error(f"Colonne manquante: {str(e)}")
        return JsonResponse({'error': f'Colonne manquante : {str(e)}'}, status=400)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)

def sms_pro_bar_line(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMos 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        # Récupérer le nom de la feuille à partir des paramètres GET
        sheet_name = request.GET.get('sheet')
        logger.info(f"Nom de la feuille demandé : {sheet_name}")
        
        # Vérifiez si le nom de la feuille est dans le fichier Excel
        xls = pd.ExcelFile(file_path)
        if sheet_name not in xls.sheet_names:
            logger.error(f"Feuille non trouvée : {sheet_name}")
            return JsonResponse({'error': 'Feuille non trouvée dans le fichier Excel.'}, status=400)

        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Total', 'Success % without exclusion', 'Date']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Total'] = df['Total'].fillna(0)
        df['Success % without exclusion'] = df['Success % without exclusion'].fillna(0)
        df['Date'] = df['Date'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Total'].tolist()
        line_data = df['Success % without exclusion'].tolist()
        labels = df['Date'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)

#SMS
def sms_datatable(request):
    file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')

    # Récupérer la dernière feuille ajoutée
    sheet_name = get_latest_sheet(file_path)

    # Récupérer la feuille précédente
    previous_sheet_name = get_previous_sheet(file_path, sheet_name)

    # Lire les données de la dernière feuille ajoutée
    df_normal = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=0)

    # Lire les données de la feuille précédente (s'il y en a une)
    if previous_sheet_name:
        df_error = pd.read_excel(file_path, sheet_name=previous_sheet_name, skiprows=0)
    else:
        df_error = pd.DataFrame()  # Crée un DataFrame vide si aucune feuille précédente n'existe

    # Traiter les colonnes datetime pour les deux DataFrames
    for df in [df_normal, df_error]:
        date_columns = df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        df.fillna({col: pd.Timestamp.now() for col in date_columns}, inplace=True)

    # Convertir les DataFrames en dictionnaires
    data_normal = df_normal.to_dict(orient='records')
    headers_normal = list(df_normal.columns)
    data_error = df_error.to_dict(orient='records')
    headers_error = list(df_error.columns)

    # Passer les deux ensembles de données au template
    context = {
        'data_normal': data_normal,
        'headers_normal': headers_normal,
        'data_error': data_error,
        'headers_error': headers_error,
    }

    return render(request, 'dashboard/page/application/vas_cloud/sms.html', context)

def sms_pie(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Success_A2P', 'Error_A2P', 'Total']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Calculer les valeurs totales
        success_total = df['Success_A2P'].sum()
        error_total = df['Error_A2P'].sum()
        grand_total = df['Total'].sum()

        # Calculer les pourcentages
        success_percentage = (success_total / grand_total) * 100 if grand_total else 0
        error_percentage = (error_total / grand_total) * 100 if grand_total else 0
        # Le reste est la différence jusqu'à 100%
        # remaining_percentage = 100 - success_percentage - error_percentage
        
        # Arrondir les pourcentages au dixième
        success_percentage = round(success_percentage, 1)
        error_percentage = round(error_percentage, 1)
        
        # Préparer les données pour le graphique circulaire
        data = [success_percentage, error_percentage]
        labels = ['Total Success Percent', 'Total Error Percent']
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def sms_pie_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24 error'  # Vous pouvez utiliser get_latest_sheet(file_path) si nécessaire
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Description', '%']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Extraire les colonnes 'Description' et '%' sous forme de listes
        descriptions = df['Description'].tolist()  # Convertir en liste
        percentages = df['%'].tolist()  # Convertir en liste et s'assurer qu'elles sont des float
        
        # Arrondir les pourcentages au dixième (facultatif)
        percentages = [round(p, 1) for p in percentages]
        
        # Préparer les données pour le graphique circulaire
        response = {
            'data': percentages,
            'labels': descriptions
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def sms_area(request):
    try:
        # Chemin vers le fichier Excel
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        # Récupération du nom de la feuille depuis les paramètres GET
        sheet_name = request.GET.get('sheet', 'Aug 24')
        print(f"Feuille sélectionnée : {sheet_name}") # Utiliser 'Aug 24' comme feuille par défaut si aucune n'est spécifiée
        
        # Chargement de la feuille Excel spécifiée
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Date', 'Success % with exclusion']
        for col in required_columns:
            if col not in df.columns:
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par des valeurs par défaut appropriées
        df['Date'] = df['Date'].fillna(method='ffill')  # Remplit les valeurs manquantes avec la dernière valeur connue
        df['Success % with exclusion'] = df['Success % with exclusion'].fillna(0) 
        
        # Conversion de la colonne 'Date' au format de chaîne approprié
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d/%m/%Y')  # Format de date ajusté
        
        # Extraction des données
        labels = df['Date'].tolist()
        line_data = df['Success % with exclusion'].tolist()
        
        response = {
            'labels': labels,
            'line_data': line_data
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def sms_bar(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'donnees_produits.xls')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        resultat = df.groupby('Category')['UnitsInStock'].sum()
        
        data = resultat.values.tolist()
        labels = resultat.index.tolist()
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

logger = logging.getLogger(__name__)

def sms_bar_line_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name =  'Aug 24 error' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Nombre', '%', 'Description']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Nombre'] = df['Nombre'].fillna(0)
        df['%'] = df['%'].fillna(0)
        df['Description'] = df['Description'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Nombre'].tolist()
        line_data = df['%'].tolist()
        labels = df['Description'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)
    
def sms_bar_line(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Total', 'Success % without exclusion', 'Date']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Total'] = df['Total'].fillna(0)
        df['Success % without exclusion'] = df['Success % without exclusion'].fillna(0)
        df['Date'] = df['Date'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Total'].tolist()
        line_data = df['Success % without exclusion'].tolist()
        labels = df['Date'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)

#USSD
def ussd_datatable(request):
    try:
        # Chemin vers le fichier Excel
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')

        if not os.path.exists(file_path):
            return render(request, 'dashboard/page/application/vas_cloud/ussd.html', {
                'error': "Le fichier Excel n'existe pas."
            })

        # Lire les données de la dernière feuille ajoutée (feuille par défaut)
        df_normal = pd.read_excel(file_path)

        # Traiter les colonnes datetime pour df_normal
        date_columns = df_normal.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns
        for col in date_columns:
            df_normal[col] = pd.to_datetime(df_normal[col], errors='coerce')
        
        # Remplir les valeurs manquantes dans les colonnes datetime
        df_normal.fillna({col: pd.Timestamp.now() for col in date_columns}, inplace=True)

        # Convertir le DataFrame en dictionnaire pour le template
        data_normal = df_normal.to_dict(orient='records')
        headers_normal = list(df_normal.columns)
        
        # Passer les données au template
        context = {
            'data_normal': data_normal,
            'headers_normal': headers_normal,
        }

        return render(request, 'dashboard/page/application/vas_cloud/ussd.html', context)
    
    except Exception as e:
        return render(request, 'dashboard/page/application/vas_cloud/ussd.html', {
            'error': str(e)
        })


def ussd_pie(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Success_A2P', 'Error_A2P', 'Total']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Calculer les valeurs totales
        success_total = df['Success_A2P'].sum()
        error_total = df['Error_A2P'].sum()
        grand_total = df['Total'].sum()

        # Calculer les pourcentages
        success_percentage = (success_total / grand_total) * 100 if grand_total else 0
        error_percentage = (error_total / grand_total) * 100 if grand_total else 0
        # Le reste est la différence jusqu'à 100%
        # remaining_percentage = 100 - success_percentage - error_percentage
        
        # Arrondir les pourcentages au dixième
        success_percentage = round(success_percentage, 1)
        error_percentage = round(error_percentage, 1)
        
        # Préparer les données pour le graphique circulaire
        data = [success_percentage, error_percentage]
        labels = ['Total Success Percent', 'Total Error Percent']
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def ussd_pie_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24 error'  # Vous pouvez utiliser get_latest_sheet(file_path) si nécessaire
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['Description', '%']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({'error': 'Les colonnes nécessaires n\'existent pas dans le fichier Excel.'}, status=400)
        
        # Extraire les colonnes 'Description' et '%' sous forme de listes
        descriptions = df['Description'].tolist()  # Convertir en liste
        percentages = df['%'].tolist()  # Convertir en liste et s'assurer qu'elles sont des float
        
        # Arrondir les pourcentages au dixième (facultatif)
        percentages = [round(p, 1) for p in percentages]
        
        # Préparer les données pour le graphique circulaire
        response = {
            'data': percentages,
            'labels': descriptions
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def ussd_area(request):
    try:
        # Chemin vers le fichier Excel
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'donnees_normales.xlsx')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        # Charger la feuille Excel
        df = pd.read_excel(file_path)
        
        # Vérifier que les colonnes nécessaires sont présentes
        required_columns = ['Date', 'Success % with exclusion']
        for col in required_columns:
            if col not in df.columns:
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN dans les colonnes pertinentes
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce').fillna(method='ffill')
        df['Success % with exclusion'] = df['Success % with exclusion'].fillna(0)
        
        # Récupérer les paramètres de dates depuis la requête GET
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if start_date and end_date:
            # Convertir les dates en objets datetime
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            
            # Filtrer les données en fonction de la plage de dates
            df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        
        # Convertir les dates en chaîne de caractères au format désiré
        df['Date'] = df['Date'].dt.strftime('%d/%m/%Y')
        
        # Extraction des données pour le graphique
        labels = df['Date'].tolist()
        line_data = df['Success % with exclusion'].tolist()
        
        response = {
            'labels': labels,
            'line_data': line_data
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def ussd_bar(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'donnees_produits.xls')
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        df = pd.read_excel(file_path)
        
        resultat = df.groupby('Category')['UnitsInStock'].sum()
        
        data = resultat.values.tolist()
        labels = resultat.index.tolist()
        
        response = {
            'data': data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

logger = logging.getLogger(__name__)

def ussd_bar_line_error(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name =  'Aug 24 error' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Nombre', '%', 'Description']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Nombre'] = df['Nombre'].fillna(0)
        df['%'] = df['%'].fillna(0)
        df['Description'] = df['Description'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Nombre'].tolist()
        line_data = df['%'].tolist()
        labels = df['Description'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)
    
def ussd_bar_line(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Dashboard', 'static', 'xlxs', 'StatsMoMo 2024.xlsx')
        
        if not os.path.exists(file_path):
            logger.error(f"Le fichier Excel n'existe pas à l'emplacement : {file_path}")
            return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
        
        sheet_name = 'Aug 24' #get_latest_sheet(file_path)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        required_columns = ['Total', 'Success % without exclusion', 'Date']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Colonne manquante : {col}")
                return JsonResponse({'error': f'Colonne manquante dans le fichier Excel : {col}'}, status=400)
        
        # Remplacer les valeurs NaN par 0 ou une autre valeur par défaut
        df['Total'] = df['Total'].fillna(0)
        df['Success % without exclusion'] = df['Success % without exclusion'].fillna(0)
        df['Date'] = df['Date'].fillna('Inconnu')  # Utiliser 'Inconnu' ou une autre valeur par défaut pour les labels
        
        # Extraire les données pour les graphiques
        bar_data = df['Total'].tolist()
        line_data = df['Success % without exclusion'].tolist()
        labels = df['Date'].tolist()
        
        response = {
            'bar_data': bar_data,
            'line_data': line_data,
            'labels': labels
        }
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        return JsonResponse({'error': 'Le fichier Excel n\'existe pas.'}, status=404)
    except Exception as e:
        logger.exception("Une erreur s'est produite lors du traitement des données Excel.")
        return JsonResponse({'error': str(e)}, status=500)

def dashboard_view(request):
    if request.user.is_authenticated:
        unread_notification_count = Notification.objects.filter(user=request.user, read=False).count()
        notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    else:
        unread_notification_count = 0
        notifications = []

    context = {
        'unread_notification_count': unread_notification_count,
        'notifications': notifications,
    }
    return render(request, 'dashboard/acceuil.html', 'dashboard/page/charts.html', context)