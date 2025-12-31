import os
import requests
import yaml

URL = "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Clash.yaml"
OUT = "rules/AWAvenue.list"

resp = requests.get(URL, timeout=30)
resp.raise_for_status()

data = yaml.safe_load(resp.text)
payload = data.get("payload", [])

rules = set()

for item in payload:
    if not isinstance(item, str):
        continue

    item = item.strip()
    if not item:
        continue

    # +.example.com  → DOMAIN-SUFFIX,example.com
    if item.startswith("+."):
        rules.add(f"DOMAIN-SUFFIX,{item[2:]}")
    else:
        rules.add(f"DOMAIN,{item}")

if not rules:
    raise RuntimeError("No rules generated from AWAvenue payload")

os.makedirs(os.path.dirname(OUT), exist_ok=True)

with open(OUT, "w", encoding="utf-8") as f:
    for rule in sorted(rules):
        f.write(rule + "\n")

print(f"Generated {len(rules)} DOMAIN / DOMAIN-SUFFIX rules")
