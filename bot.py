import os, requests, time
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = os.environ.get("CANAL_ID")
AFILIADO = "gamer-a4609b2"

def enviar(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": CANAL_ID, "text": texto}, timeout=15)
        print(f"Telegram: {r.text[:200]}")
        return True
    except Exception as e:
        print(f"Error envio: {e}")
        return False

print("INICIANDO BOT")
# Manda 5 fijos para probar que funciona
juegos = [
    "🔥 Elden Ring EN OFERTA\n💸 https://www.instant-gaming.com/es/12345-buy-elden-ring/?igr=gamer-a4609b2",
    "🔥 GTA V EN OFERTA\n💸 https://www.instant-gaming.com/es/789-buy-grand-theft-auto-v/?igr=gamer-a4609b2",
    "🔥 Red Dead Redemption 2 EN OFERTA\n💸 https://www.instant-gaming.com/es/2546-buy-red-dead-redemption-2/?igr=gamer-a4609b2",
    "🎮 GRATIS HOY: Revisa Epic Games Store\n💸 Juegos baratos: https://www.instant-gaming.com/es/?igr=gamer-a4609b2",
    "🎮 GRATIS HOY: Juegos gratis en Steam\n💸 Más baratos: https://www.instant-gaming.com/es/?igr=gamer-a4609b2"
]

for j in juegos:
    enviar(j)
    time.sleep(6)

print("FIN TOTAL - 5 enviados")
