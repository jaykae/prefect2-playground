import json
import os
import requests

with open("workpool.json","r") as f:
    data = json.load(f)

api_url = os.getenv("PREFECT_API_URL")
result = requests.post(os.path.join(api_url,"work_pools"), json=data, timeout=30)

print(result.ok)