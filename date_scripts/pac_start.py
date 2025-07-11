import pandas as pd
import subprocess
import shutil
import os
import time

def get_first_commit_date_for_path(repo_full_name, file_path):
    repo_dir = "temp_repo"

    try:
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

        # Clone the repo
        subprocess.run(
            ["git", "clone", "--quiet", f"https://github.com/{repo_full_name}.git", repo_dir],
            check=True
        )

        # Use git log to find the first commit that touched the file
        sha = subprocess.check_output(
            ["git", "-C", repo_dir, "log", "--diff-filter=A", "--format=%H", "--", file_path],
            stderr=subprocess.DEVNULL
        ).decode().strip()

        if not sha:
            return "Not found"

        # Get the date of that commit
        date = subprocess.check_output(
            ["git", "-C", repo_dir, "show", "-s", "--format=%cI", sha]
        ).decode().strip()

        return date

    except Exception as e:
        print(f"❌ Error for {repo_full_name} - {file_path}: {e}")
        return "Error"

    finally:
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

# === Load CSV ===
df = pd.read_csv("compiled.csv")

# Add introduced_at column if missing
if "introduced_at" not in df.columns:
    df["introduced_at"] = pd.Series(dtype="object")

try:
    for i, row in df.iterrows():
        if pd.notna(row["introduced_at"]):
            continue

        repo = row["repo_name"]           
        path = row["path"]                
        print(f"🔍 Getting first commit for {repo} — file: {path}...")
        date = get_first_commit_date_for_path(repo, path)
        df.at[i, "introduced_at"] = date
        print(f"✅ {repo} — {path} introduced at: {date}")
        time.sleep(1)

except KeyboardInterrupt:
    print("🛑 Interrupted. Saving progress...")

finally:
    df.to_csv("compiled_pac.csv", index=False)
    print("💾 Saved to with_introduced_dates.csv")
