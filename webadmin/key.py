import requests



link = 'http://127.0.0.1:8000/update_status/2'

print(requests.post(link).text)