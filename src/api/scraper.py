from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import sqlite3
import time

# URL cible
URL = "https://immobilier.lefigaro.fr/annonces/immobilier-entreprise-location"

def get_annonces():
    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(URL)
    time.sleep(10)  # Laisser le temps au site de charger
    annonces = driver.find_elements(By.CSS_SELECTOR, "div.some-annonce-class")

    extracted_data = []
    for annonce in annonces:
        try:
            title = annonce.find_element(By.TAG_NAME, "h2").text.strip()
            price = annonce.find_element(By.CLASS_NAME, "price").text.strip()
            location = annonce.find_element(By.CLASS_NAME, "location").text.strip()
            link = annonce.find_element(By.TAG_NAME, "a").get_attribute("href")

            extracted_data.append({
                "titre": title,
                "prix": price,
                "localisation": location,
                "lien": link
            })
        except:
            continue

    driver.quit()
    return extracted_data

def save_annonces(annonces):
    db_conn = sqlite3.connect("leads.db")
    cursor = db_conn.cursor()

    for annonce in annonces:
        cursor.execute("""
            INSERT INTO real_estate_transactions (title, company, location, transaction_type, date, source)
            VALUES (?, ?, ?, ?, DATE('now'), ?)
        """, (annonce["titre"], "Non précisé", annonce["localisation"], "Location", annonce["lien"]))

    db_conn.commit()
    db_conn.close()
    print(f"{len(annonces)} annonces enregistrées en base.")

if __name__ == "__main__":
    annonces = get_annonces()
    if annonces:
        print(annonces)
        save_annonces(annonces)
        print("Scraping terminé avec succès !")
    else:
        print("Aucune annonce récupérée.")
