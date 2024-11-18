import os
import json
import xml.etree.ElementTree as ET
import requests

# Define the folder path
FOLDER_PATH = r"C:\repos"

# SonarQube server URL and authentication
SONARQUBE_URL = 'http://localhost:9090/issues?issueStatuses=OPEN%2CCONFIRMED'  # Use a relevant API endpoint
SONARQUBE_USER = 'ad'  # Replace with your username
SONARQUBE_PASSWORD = 'Admin'  # Replace with your password

# Function to send a file to SonarQube
def send_file_to_sonarqube(file_path, content_type):
    with open(file_path, 'rb') as file:
        headers = {
            'Content-Type': content_type
        }
        response = requests.post(SONARQUBE_URL, headers=headers, auth=(SONARQUBE_USER, SONARQUBE_PASSWORD), data=file)

        if response.status_code == 200:
            print(f"File '{os.path.basename(file_path)}' sent successfully to SonarQube.")
        else:
            print(f"Failed to send file '{os.path.basename(file_path)}' to SonarQube. Status code: {response.status_code}")
            print(f"Response: {response.text}")

# Main function to iterate through the folder and send files to SonarQube
def send_files_to_sonarqube(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if filename.endswith(".json"):
            try:
                # Check if the JSON is valid before sending
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    json.load(json_file)  # This will raise an error if JSON is invalid
                send_file_to_sonarqube(file_path, 'application/json')
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON file '{filename}': {e}")

        elif filename.endswith(".xml"):
            try:
                # Check if the XML is valid before sending
                with open(file_path, 'r', encoding='utf-8') as xml_file:
                    ET.parse(xml_file)  # This will raise an error if XML is invalid
                send_file_to_sonarqube(file_path, 'application/xml')
            except ET.ParseError as e:
                print(f"Failed to parse XML file '{filename}': {e}")

# Run the script
send_files_to_sonarqube(FOLDER_PATH)

sqp_f78377e1ca1a254c72c30a3df1bf29da131db5ff

