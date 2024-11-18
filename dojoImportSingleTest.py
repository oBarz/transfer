import os
import requests
import json
from collections import defaultdict
from datetime import datetime

# Configuration
DEFECTDOJO_URL = "http://localhost:8080"  # Update with your DefectDojo URL
API_KEY = "a467c2346e3cb9cf9bc7b34e506008572a6cc3bf"  # Replace with your API key
ENGAGEMENT_ID = 17  # Replace with your engagement ID
PRODUCT_ID = 16  # Replace with your product ID
FOLDER_PATH = r"C:\dojo\repos"  # Path to the folder containing SARIF files

# Headers for authentication
headers = {
    "Authorization": f"Token {API_KEY}",
    "Accept": "application/json",
}

# Function to parse SARIF file and extract relevant data
def parse_sarif(file_path):
    with open(file_path, 'r') as file:
        sarif_data = json.load(file)
        findings = []
        for run in sarif_data.get("runs", []):
            for result in run.get("results", []):
                finding = {
                    "vulnerability_id": result["ruleId"],
                    "severity": result["level"],
                    "sla": result.get("suppressions", [{}])[0].get("justification", "N/A"),
                    "file_path": file_path,
                    "date": datetime.fromtimestamp(os.path.getmtime(file_path)),
                }
                findings.append(finding)
        return findings

# Step 1: Gather all findings from all SARIF files
findings_by_key = defaultdict(list)
for filename in os.listdir(FOLDER_PATH):
    if filename.endswith(".sarif"):
        file_path = os.path.join(FOLDER_PATH, filename)
        findings = parse_sarif(file_path)
        for finding in findings:
            key = (finding["vulnerability_id"], finding["severity"], finding["sla"])
            findings_by_key[key].append(finding)

# Step 2: Select the most recent finding for each key
unique_findings = []
for key, findings in findings_by_key.items():
    most_recent_finding = max(findings, key=lambda x: x["date"])
    unique_findings.append(most_recent_finding)

# Step 3: Import unique findings into DefectDojo
for finding in unique_findings:
    file_path = finding["file_path"]
    with open(file_path, 'rb') as sarif_file:
        files = {'file': sarif_file}
        upload_url = f"{DEFECTDOJO_URL}/api/v2/import-scan/"
        data = {
            "scan_type": "SARIF",
            "engagement": ENGAGEMENT_ID,
            "product_type": PRODUCT_ID,
            "close_old_findings": False,
            "skip_duplicates": False,
            "scan_date": "2024-08-27",  # Update to the current date
            "tags": "sarif,api_import"
        }

        # Send the POST request to upload the SARIF file
        response = requests.post(upload_url, headers=headers, data=data, files=files)

        # Check the response status
        if response.status_code == 201:
            print(f"SARIF report '{os.path.basename(file_path)}' imported successfully!")
        else:
            print(f"Failed to import SARIF report '{os.path.basename(file_path)}': {response.status_code}")
            print(response.text)
