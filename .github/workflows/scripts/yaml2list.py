import requests
import yaml

URL = "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Clash.yaml"
OUT = "rules/AWAvenue.list"

resp = requests.get(URL, timeout=30)
resp.raise_for_status()

data = yaml.safe_load(resp.text)

payload = data.get("payload", [])

domains = set()

for rule in payload:
    if rule.startswith("DOMAIN-SUFFIX,"):
        domains.add(rule.split(",", 1)[1])
    elif rule.startswith("DOMAIN,"):
        domains.add(rule.split(",", 1)[1])

with open(OUT, "w", encoding="utf-8") as f:
    for d in sorted(domains):
        f.write(d + "\n")

print(f"Generated {len(domains)} domains")
