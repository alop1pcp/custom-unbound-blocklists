import os
import requests
from datetime import datetime, timezone

URL_TARGET = "https://raw.githubusercontent.com/alop1pcp/custom-unbound-blocklists/refs/heads/main/ddg-app-tracking-protection-blocklist.txt"
URL_SRC = "https://raw.githubusercontent.com/duckduckgo/tracker-blocklists/refs/heads/main/app/android-tds.json"
OUTPUT_DIR = "blocklists"
OUTPUT_FILE = f"{OUTPUT_DIR}/ddg-app-tracking-protection-blocklist.txt"


def get_tracker_list_from_url(url: str):
  response = requests.get(url, timeout=30)
  response.raise_for_status()
  return response

os.makedirs("blocklists", exist_ok=True)

previous_raw = get_tracker_list_from_url(URL_TARGET).text
previous_trackers = [l.strip() for l in previous_raw.splitlines() if not l.startswith("#") and l.strip() != ""]

resp = get_tracker_list_from_url(URL_SRC).json()
tracker_dict = resp["trackers"]
tracker_domains = sorted(
  k for k, v in tracker_dict.items()
  if v.get("default") == "block"
)

if previous_trackers == tracker_domains:
  with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(previous_raw)
    print("No changes")
    raise SystemExit(0)


now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
header = (
f"""# Title: DDG App Tracking Protection Blocklist
# Description: Blocklist derived from DuckDuckGo App Tracking Protection
# Homepage: https://github.com/alop1pcp/custom-unbound-blocklists
# License: MIT
# Last modified: {now}
# Format: domains
# Entries: {len(tracker_domains):,}\n
"""
)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
  f.write(header)
  for domain in tracker_domains:
    f.write(domain + "\n")

print(f"Wrote {len(tracker_domains)} domains to {OUTPUT_FILE}")
