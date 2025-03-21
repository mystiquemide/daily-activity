import subprocess
import os
from datetime import datetime, timedelta
import random

# ---- CONFIG ----
FILE_NAME   = "commits.md"
START_DATE  = datetime(2025, 3, 21)   # today
END_DATE    = datetime(2025, 3, 22)   # tomorrow (covers full today)
MIN_COMMITS = 15
MAX_COMMITS = 25
SKIP_CHANCE = 0.0
# ----------------

def run(cmd, env=None):
    result = subprocess.run(cmd, shell=True, env=env)
    if result.returncode != 0:
        print(f"⚠️  Command failed: {cmd}")
    return result.returncode

current_date = START_DATE
total = 0

while current_date <= END_DATE:

    commits_today = random.randint(MIN_COMMITS, MAX_COMMITS)

    for j in range(commits_today):
        hour   = random.randint(8, 22)
        minute = random.randint(0, 59)

        with open(FILE_NAME, "a") as f:
            f.write(
                f"- [{current_date.strftime('%Y-%m-%d')} {hour:02d}:{minute:02d}]"
                f" commit {total+1}, session {j+1}\n"
            )

        run("git add .")

        date_str = f"{current_date.strftime('%Y-%m-%d')}T{hour:02d}:{minute:02d}:00"
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"]    = date_str
        env["GIT_COMMITTER_DATE"] = date_str

        code = run(
            f'git commit -m "chore: update log {current_date.strftime("%Y-%m-%d")} #{j+1}"',
            env=env
        )

        if code == 0:
            total += 1
            print(f"✅ Commit {total} — {current_date.strftime('%Y-%m-%d')} {hour:02d}:{minute:02d}")

    current_date += timedelta(days=1)

print(f"\n🎯 Total commits created: {total}")
print("🚀 Pushing to GitHub...")
run("git push origin main")
print("✅ Done! Check your GitHub contribution graph.")
