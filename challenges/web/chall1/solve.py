import requests

url = "http://challenge:5000/debug?admin=1"

r = requests.get(url)

if "flag" in r.text:
    print(r.text.strip())
    exit(0)

print("FAILED: flag not found", flush=True)
exit(1)
