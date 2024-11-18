import os
import requests
import json

# Configurație
DEFECTDOJO_URL = "http://localhost:8080"  # Actualizează cu URL-ul DefectDojo
API_KEY = "a467c2346e3cb9cf9bc7b34e506008572a6cc3bf"  # Înlocuiește cu API key-ul tău
ENGAGEMENT_ID = 18  # Înlocuiește cu ID-ul tău de engagement
PRODUCT_ID = 17  # Înlocuiește cu ID-ul tău de produs
FOLDER_PATH = r"C:\dojo\repos"  # Calea către folderul care conține fișierele SARIF

# Headers pentru autentificare
headers = {
    "Authorization": f"Token {API_KEY}",
    "Accept": "application/json",
}

# Pasul 1: Iterare prin toate fișierele SARIF din folder
for filename in os.listdir(FOLDER_PATH):
    if filename.endswith(".sarif"):
        file_path = os.path.join(FOLDER_PATH, filename)
        
        # Eliminăm extensia din numele fișierului pentru a folosi ca titlu și nume test
        test_name = os.path.splitext(filename)[0]
        
        # Deschidem fișierul SARIF
        with open(file_path, 'rb') as sarif_file:
            files = {'file': sarif_file}
            upload_url = f"{DEFECTDOJO_URL}/api/v2/import-scan/"
            data = {
                "scan_type": "SARIF",
                "engagement": ENGAGEMENT_ID,
                "product_type": PRODUCT_ID,
                "close_old_findings": False,
                "skip_duplicates": True,
                "scan_date": "2024-08-27",  # Actualizează la data curentă
                "tags": "sarif,api_import",
                "test_title": test_name,  # Setăm titlul testului
                "title": test_name,  # Setăm titlul
		"active": False,
		"verified": True,
		"mitigation": "cucu bau",
		"out_of_scope": False,
		"risk_accepted": False,
		"under_review": False,
            }

            # Trimitem cererea POST pentru a încărca fișierul SARIF
            response = requests.post(upload_url, headers=headers, data=data, files=files)

            # Verificăm statusul răspunsului
            if response.status_code == 201:
                print(f"Raportul SARIF '{filename}' a fost importat cu succes!")
            else:
                print(f"Importul raportului SARIF '{filename}' a eșuat: {response.status_code}")
                print(response.text)
