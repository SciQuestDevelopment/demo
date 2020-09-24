import requests

proxies = {
  "http": "http://scraperapi:c217d379d259aefb612ee3dea025c4fe@proxy-server.scraperapi.com:8001",
  "https": "http://scraperapi:c217d379d259aefb612ee3dea025c4fe@proxy-server.scraperapi.com:8001"
}

r = requests.get('https://scholar.google.com/scholar?hl=en&scisbd=1&as_sdt=0%2C33&q=computer+science&btnG=', proxies=proxies, verify=False)

print(r.text)
