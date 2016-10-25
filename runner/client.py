import requests

r = requests.post("http://127.0.0.1:5000/query", data={
    "query": "SELECT * FROM t2"
})

print(r.text)
