import pandas as pd
import requests
import time

# Load CSV
df = pd.read_csv('compiled.csv')

import subprocess

def get_github_token():
    try:
        return subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except subprocess.CalledProcessError:
        print("❌ Could not retrieve token.")
        return None
GITHUB_TOKEN = get_github_token()
URL = "https://api.github.com/graphql"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

# Filter rows that need updates
needs_update = df[df['stars'].isna() | df['latest_commit'].isna()]

for idx, row in needs_update.iterrows():
    owner_repo = row['repo_name']
    if '/' not in owner_repo:
        print(f"Invalid repo format: {owner_repo}")
        continue
    owner, repo = owner_repo.split("/")

    query = """
    query ($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        stargazerCount
        pushedAt
      }
    }
    """

    variables = {"owner": owner, "name": repo}
    response = requests.post(URL, json={"query": query, "variables": variables}, headers=HEADERS)

    if response.status_code == 200:
        result = response.json()
        repo_data = result.get("data", {}).get("repository", None)
        if repo_data:
            if pd.isna(row['stars']):
                df.at[idx, 'stars'] = repo_data.get("stargazerCount", None)
            if pd.isna(row['latest_commit']):
                df.at[idx, 'latest_commit'] = repo_data.get("pushedAt", None)
        else:
            print(f"No data for {owner_repo}")
    else:
        print(f"Failed to fetch {owner_repo}: {response.status_code}")
    

df.to_csv("compiled_last_and_stars.csv", index=False)
print("Done. Saved to updated_repos_graphql.csv")
