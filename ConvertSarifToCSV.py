import pandas as pd
import json

# Function to convert XLSX to SARIF format
def xlsx_to_sarif(xlsx_filename, sarif_filename):
    # Read the XLSX file
    df = pd.read_excel(xlsx_filename)

    sarif_data = {
        "version": "2.1.0",
        "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.5.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "SonarQube Issues to SARIF Converter",
                        "informationUri": "https://example.com",
                        "version": "1.0.0"
                    }
                },
                "results": []
            }
        ]
    }

    # Iterate over the rows in the Excel sheet
    for _, row in df.iterrows():
        # Extract lines (could be multiple) from the 'line' column
        line_values = row.get('line', '1')
        if isinstance(line_values, str):
            line_numbers = [int(x.strip()) for x in line_values.split(',')]
        else:
            line_numbers = [int(line_values)]

        # Create locations for each line
        locations = [
            {
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": row.get('component', 'N/A')  # Using 'component' as file
                    },
                    "region": {
                        "startLine": line,
                        "startColumn": 1  # Default column as 1
                    }
                }
            }
            for line in line_numbers
        ]

        # Create the result entry
        result = {
            "ruleId": row.get('rule', 'N/A'),  # Using 'rule' as the ruleId
            "level": row.get('severity', 'warning').lower(),  # Mapping 'severity' to level
            "message": {
                "text": row.get('message', 'No message provided')
            },
            "locations": locations,  # Use the list of locations for multiple lines
            "properties": {
		"key": row.get('key', 'N/A'),
		"project": row.get('project', 'N/A'),
		"line": row.get('line', 'N/A'),
		"hash": row.get('hash', 'N/A'),
		"textRange": row.get('textRange', 'N/A'),
		"flows": row.get('flows', 'N/A'),
		"status": row.get('status', 'N/A'),
                "author": row.get('author', 'N/A'),
		"tags": row.get('tags', 'N/A'),
                "creationDate": row.get('creationDate', 'N/A'),
                "updateDate": row.get('updateDate', 'N/A'),
                "effort": row.get('effort', 'N/A'),
                "debt": row.get('debt', 'N/A'),
                "scope": row.get('scope', 'N/A'),
                "type": row.get('type', 'N/A'),
                "quickFixAvailable": row.get('quickFixAvailable', 'N/A'),
		"messageFormattings": row.get('messageFormattings', 'N/A'),
		"codeVariants": row.get('codeVariants', 'N/A'),
		"cleanCodeAttribute": row.get('cleanCodeAttribute', 'N/A'),
		"cleanCodeAttribute": row.get('cleanCodeAttribute', 'N/A'),
		"cleanCodeAttributeCategory": row.get('cleanCodeAttributeCategory', 'N/A'),
		"impacts": row.get('impacts', 'N/A'),
		"issueStatus": row.get('issueStatus', 'N/A'),
		"prioririzedStatus": row.get('prioririzedStatus', 'N/A')
            }
        }
        sarif_data['runs'][0]['results'].append(result)

    # Write the SARIF output to a JSON file
    with open(sarif_filename, mode='w') as sarif_file:
        json.dump(sarif_data, sarif_file, indent=4)

    print(f"SARIF file saved to {sarif_filename}")

# Usage example
xlsx_filename = 'sonarqube_issues.xlsx'
sarif_filename = 'output.sarif'

xlsx_to_sarif(xlsx_filename, sarif_filename)