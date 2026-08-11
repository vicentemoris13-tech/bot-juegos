import os, requests
TOKEN=os.environ.get("TELEGRAM_TOKEN")
CANAL=os.environ.get("CANAL_ID")
print(f"Probando canal {CANAL}")
r=requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CANAL, "text": "PRUEBA 1/1 FUNCIONA"})
print(r.text)
