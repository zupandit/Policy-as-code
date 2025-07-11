import csv
import requests
import time
import subprocess

def get_github_token():
    try:
        token = subprocess.check_output(
            ["gh", "auth", "token"], text=True
        ).strip()
        return token
    except subprocess.CalledProcessError:
        print("Could not retrieve token from GitHub CLI.")
        return None


GITHUB_TOKEN = get_github_token()

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

input_file = "repos.csv"
output_file = "repo_with_ids.csv"

with open(input_file, newline='') as csvfile_in, open(output_file, 'w', newline='') as csvfile_out:
    print("entered")
    reader = csv.DictReader(csvfile_in)
    fieldnames = reader.fieldnames + ['repo_id']
    writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
    writer.writeheader()

    i = 0
    for row in reader:
        repo_name = row['repo_name']
        try:
            response = requests.get(f"https://api.github.com/repos/{repo_name}", headers=headers)
            if response.status_code == 200:
                print("Succes: ", i)
                data = response.json()
                row['repo_id'] = data['id']
            else:
                print(f"Failed to fetch {repo_name}: {response.status_code}")
                row['repo_id'] = 'N/A'
        except Exception as e:
            print(f"Error for {repo_name}: {e}")
            row['repo_id'] = 'N/A'
        
        writer.writerow(row)
        i +=1
