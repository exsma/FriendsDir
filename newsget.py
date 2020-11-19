import http.client

conn = http.client.HTTPSConnection("rapidapi.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "0c955f83a1msh510ad75dec49888p1b8b41jsn889f39daf050",
    'x-rapidapi-host': "google-news.p.rapidapi.com"
    }

conn.request("GET", "/v1/geo_headlines?geo="+ City, headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))