import os
import requests
import yaml

URL = "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Clash.yaml"
OUT = "rules/AWAvenue.list"

resp = requests.get(URL, timeout=30)
resp.raise_for_status()

data = yaml.safe_load(resp.text)

payload = data.get("payload", [])

# payload 应该是一个字符串列表
domains = set()

for item in payload:
    if isinstance(item, str) and item.strip():
        domains.add(item.strip())

if not domains:
    raise RuntimeError("AWAvenue payload is empty or invalid")

os.makedirs(os.path.dirname(OUT), exist_ok=True)

with open(OUT, "w", encoding="utf-8") as f:
    for d in sorted(domains):
        f.write(d + "\n")

print(f"Generated {len(domains)} domains from AWAvenue payload")
