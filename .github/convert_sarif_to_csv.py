import json
import csv

# Load the SARIF file
with open('codeql-results for location in locations:
            physical_location = location.get('physicalLocation', {})
            artifact_location = physical_location.get('artifactLocation', {})
            file_path = artifact_location.get('uri', '')
            region = physical_location.get('region', {})
            start_line = region.get('startLine', '')
            results.append({
                'Tool': tool,
                'Rule ID': rule_id,
                'Message': message,
                'File Path': file_path,
                'Start Line': start_line
            })

# Write to CSV
csv_file = 'codeql_issues.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Tool', 'Rule ID', 'Message', 'File Path', 'Start Line'])
    writer.writeheader()
    writer.writerows(results)

print(f"✅ CodeQL issues have been written to {csv_file}")
with open('codeql-results.sarif', 'r') as file:
    sarif_data = json.load(file)

# Extract relevant issue details
results = []
runs = sarif_data.get('runs', [])
for run in runs:
    tool = run.get('tool', {}).get('driver', {}).get('name', '')
    for result in run.get('results', []):
        rule_id = result.get('ruleId', '')
        message = result.get('message', {}).get('text', '')
        locations = result.get('locations', [])
       