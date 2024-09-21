import subprocess
import os
from datetime import datetime, timedelta
import random

# ---- CONFIG ----
FILE_NAME  = "log.md"
START_DATE = datetime(2024, 9, 21)   # 6 months ago
END_DATE   = datetime(2025, 3, 21)   # today
MIN_COMMITS = 1                       # minimum commits per day
MAX_COMMITS = 6                       # maximum commits per day
SKIP_DAYS   = 0.15                    # 15% chance of skipping a day (rest day)
# ----------------

def run(cmd, env=None):
    subprocess.run(cmd, shell=True, check=True, env=env)

current_date = START_DATE
total = 0

while current_date <= END_DATE:

    # randomly skip some days to look human
    if random.random() < SKIP_DAYS:
        print(f"⏭️  Skipped {current_date.strftime('%Y-%m-%d')}")
        current_date += timedelta(days=1)
        continue

    # random number of commits for this day
    commits_today = random.randint(MIN_COMMITS, MAX_COMMITS)

    for j in range(commits_today):
        # randomize the hour slightly per commit
        hour   = random.randint(8, 22)
        minute = random.randint(0, 59)

        with open(FILE_NAME, "a") as f:
            f.write(
                f"[{current_date.strftime('%Y-%m-%d')} {hour:02d}:{minute:02d}]"
                f" session {j+1} — entry {total+1}\n"
            )

        run("git add .")

        date_str = current_date.strftime(f"%Y-%m-%dT{hour:02d}:{minute:02d}:00")
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"]    = date_str
        env["GIT_COMMITTER_DATE"] = date_str

        run(
            f'git commit -m "update: {current_date.strftime("%Y-%m-%d")} #{j+1}"',
            env=env
        )
        total += 1
        print(f"✅ Commit {total} — {current_date.strftime('%Y-%m-%d')} at {hour:02d}:{minute:02d}")

    current_date += timedelta(days=1)

print(f"\n🎯 Total commits: {total}")
print("🚀 Pushing to GitHub...")
run("git push -u origin main")
print("✅ All done! Check your GitHub contribution graph.")
