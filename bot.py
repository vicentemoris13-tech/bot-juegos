import os, requests, asyncio
from telegram import Bot

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = os.environ.get("CANAL_ID")
AFILIADO = "gamer-a4609b2"
bot = Bot(token=TOKEN)

HEADERS = {"User-Agent": "Mozilla/5.0"}

async def enviar(texto):
    try:
        await bot.send_message(chat_id=CANAL_ID, text=texto)
        print(f"OK enviado: {texto[:30]}")
        return True
    except Exception as e:
        print(f"ERROR enviando: {e}")
        return False

async def main():
    print("INICIANDO BOT")
    enviados = 0

    # Intentar 3 de CheapShark con headers
    try:
        url = "https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15&pageSize=3"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        print(f"CheapShark status: {resp.status_code} len: {len(resp.text)}")
        data = resp.json()
        for d in data[:3]:
            if isinstance(d, dict):
                nombre = d.get('title','Juego')
                link = f"https://www.instant-gaming.com/es/buscar/?q={nombre.replace(' ', '+')}&igr={AFILIADO}"
                msg = f"🔥 {nombre} {int(float(d.get('savings',0)))}% OFF\n${d.get('normalPrice')} -> ${d.get('salePrice')}\n💸 Más barato: {link}"
                if await enviar(msg):
                    enviados+=1
                await asyncio.sleep(6)
    except Exception as e:
        print(f"Fallo ofertas: {e}")

    # Fallback si no mandó 3 - manda fijos
    if enviados < 3:
        print("Usando fallback baratos")
        for nombre in ["Elden Ring", "GTA V", "Red Dead Redemption 2"][:3-enviados]:
            link = f"https://www.instant-gaming.com/es/buscar/?q={nombre.replace(' ', '+')}&igr={AFILIADO}"
            await enviar(f"🔥 {nombre} EN OFERTA\n💸 Más barato: {link}")
            await asyncio.sleep(5)

    # Gratis Epic con headers
    try:
        url2 = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromos?locale=es-ES&country=CL"
        resp2 = requests.get(url2, headers=HEADERS, timeout=15)
        print(f"Epic status: {resp2.status_code}")
        j = resp2.json()
        elementos = j['data']['Catalog']['searchStore']['elements']
        c=0
        for elem in elementos:
            if c>=2: break
            promo = elem.get('promotions')
            if promo and promo.get('promotionalOffers'):
                t = elem['title']
                link = f"https://www.instant-gaming.com/es/buscar/?q={t.replace(' ', '+')}&igr={AFILIADO}"
                await enviar(f"🎮 ¡GRATIS! {t}\n💸 Versión barata: {link}")
                c+=1
                await asyncio.sleep(5)
    except Exception as e:
        print(f"Fallo gratis: {e}")
        # Fallback gratis
        await enviar(f"🎮 ¡GRATIS! Revisa Epic Games hoy\n💸 Más barato en IG: https://www.instant-gaming.com/es/?igr={AFILIADO}")
        await enviar(f"🎮 ¡GRATIS! También en Steam gratis a veces\n💸 Más barato: https://www.instant-gaming.com/es/?igr={AFILIADO}")

    print("FIN TOTAL")

asyncio.run(main())
