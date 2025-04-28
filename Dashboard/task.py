# app/tasks.py
# my_app/tasks.py
from celery import shared_task
from .Service.scraper import main

@shared_task
def run_scraping_task():
    url = "http://10.10.50.9/#/hdm/cpe"
    main(url)  # Exécute le scraping
