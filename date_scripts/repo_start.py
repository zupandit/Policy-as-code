import pandas as pd
import subprocess
import shutil
import os
import time

def get_first_commit_date_git(repo_full_name):
    repo_dir = "temp_repo"

    try:
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

        subprocess.run(
            ["git", "clone", "--quiet", f"https://github.com/{repo_full_name}.git", repo_dir],
            check=True
        )

        # Get all root commits (multiple SHAs if unrelated histories)
        sha_output = subprocess.check_output(
            ["git", "-C", repo_dir, "rev-list", "--max-parents=0", "HEAD"]
        ).decode().strip().splitlines()

        # Pick the oldest commit (first in list)
        first_sha = sha_output[0]

        # Get commit date
        date = subprocess.check_output(
            ["git", "-C", repo_dir, "show", "-s", "--format=%cI", first_sha]
        ).decode().strip()

        return date

    except Exception as e:
        print(f"❌ Error for {repo_full_name}: {e}")
        return "Error"

    finally:
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)


# === Main Script ===
df = pd.read_csv("compiled.csv")

if "first_commit" not in df.columns:
    df["first_commit"] = pd.Series(dtype="object")

try:
    for i, row in df.iterrows():
        if pd.notna(row["first_commit"]):
            continue

        repo = row["repo_name"]  
        print(f"🔍 Getting first commit for {repo}...")
        date = get_first_commit_date_git(repo)
        df.at[i, "first_commit"] = date
        print(f"✅ {repo} — First commit: {date}")
        time.sleep(1)

except KeyboardInterrupt:
    print("🛑 Interrupted. Saving progress...")

finally:
    df.to_csv("compiled_first.csv", index=False)
    print("💾 Progress saved to with_first_commits.csv")
