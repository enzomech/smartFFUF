import subprocess
import json
import requests
import os
import argparse
from tqdm import tqdm

DEFAULT_WORDLIST = "/usr/share/wordlists/seclists/Discovery/Web-Content/big.txt"
FFUF_OUT = "ffuf.json"

# ---------------- CLI ARGUMENTS ----------------

parser = argparse.ArgumentParser(
    description="smartFFUF - Minimal Python wrapper around FFUF with post-filtering",
    usage="python smartFFUF.py <IP> [options]"
)

parser.add_argument("ip", help="Target IP or host (without http)")
parser.add_argument("-fc", "--filter-codes", help="Status codes to ignore in ffuf (ex: 301,403)")
parser.add_argument("-x", "--exclude", help="String to exclude from response body")
parser.add_argument(
    "-w", "--wordlist",
    default=DEFAULT_WORDLIST,
    help="Custom wordlist (default: built-in path)"
)
parser.add_argument(
    "-json", "--json-output",
    action="store_true",
    help="Generate urlsFiltered.json output file"
)

args = parser.parse_args()

IP = "http://" + args.ip
WORDLIST = args.wordlist
exclude_filter = args.exclude
filter_codes = args.filter_codes
json_output = args.json_output

# ---------------- RUN FFUF ----------------

print("[*] Running ffuf...")

ffuf_cmd = [
    "ffuf",
    "-w", WORDLIST,
    "-u", f"{IP}/FUZZ",
    "-o", FFUF_OUT,
    "-of", "json"
]

if filter_codes:
    ffuf_cmd.extend(["-fc", filter_codes])

subprocess.run(ffuf_cmd, stdout=subprocess.DEVNULL)

# ---------------- PARSE FFUF ----------------

print("[*] Parsing ffuf results...")
with open(FFUF_OUT) as f:
    data = json.load(f)

paths = [r["input"]["FUZZ"] for r in data["results"]]
print(f"[*] {len(paths)} paths kept by ffuf")

# ---------------- FILTERING ----------------

print("[*] Filtering responses...")
filtered_results = []

for path in tqdm(paths, desc="Filtering", unit="url"):
    url = f"{IP}/{path}"
    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        status = r.status_code
        length = len(r.content)
        body = r.text

        if exclude_filter and exclude_filter in body:
            continue

        filtered_results.append({
            "path": path,
            "status": status,
            "length": length
        })

    except:
        pass

# ---------------- OUTPUT ----------------

print("\n[*] Filtered results:\n")
for r in filtered_results:
    print(f"{r['path']} | {r['status']} | {r['length']}")

with open("urlsFiltered.txt", "w") as f:
    for r in filtered_results:
        f.write(f"{r['path']} | {r['status']} | {r['length']}\n")

print("\n[*] Results saved to urlsFiltered.txt")

if json_output:
    with open("urlsFiltered.json", "w") as f:
        json.dump(filtered_results, f, indent=4)
    print("[*] JSON results saved to urlsFiltered.json")

# ---------------- CLEANUP ----------------

if os.path.exists(FFUF_OUT):
    os.remove(FFUF_OUT)

print("[*] Temporary files removed")
