import asyncio, os, requests
from telegram import Bot

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = os.environ.get("CANAL_ID")
AFILIADO = "gamer-a4609b2"
bot = Bot(token=TOKEN)

async def enviar(texto):
    try:
        await bot.send_message(chat_id=CANAL_ID, text=texto)
        print("OK enviado")
        return True
    except Exception as e:
        print(f"ERROR enviando: {e}")
        return False

async def main():
    print(f"Iniciando para canal {CANAL_ID}")
    
    # 3 baratos Steam
    try:
        r = requests.get("https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15&pageSize=3", timeout=15).json()
        for d in r:
            nombre = d['title']
            link = f"https://www.instant-gaming.com/es/buscar/?q={nombre.replace(' ', '+')}&igr={AFILIADO}"
            msg = f"🔥 {nombre} {int(float(d['savings']))}% OFF\n${d['normalPrice']} -> ${d['salePrice']}\n👉 Steam: https://store.steampowered.com/app/{d['steamAppID']}/\n💸 Más barato: {link}"
            await enviar(msg)
            await asyncio.sleep(8)
    except Exception as e:
        print(f"Fallo ofertas: {e}")

    # 2 gratis Epic
    try:
        r = requests.get("https://store-site-backend-static.ak.epicgames.com/freeGamesPromos?locale=es-ES&country=CL", timeout=15).json()
        elementos = r['data']['Catalog']['searchStore']['elements']
        c = 0
        for j in elementos:
            if c >= 2: break
            if j.get('promotions') and j['promotions']['promotionalOffers']:
                t = j['title']
                link = f"https://www.instant-gaming.com/es/buscar/?q={t.replace(' ', '+')}&igr={AFILIADO}"
                msg = f"🎮 ¡GRATIS! {t}\n💸 Versión barata Steam: {link}"
                await enviar(msg)
                c+=1
                await asyncio.sleep(8)
    except Exception as e:
        print(f"Fallo gratis: {e}")

    print("FIN TOTAL")

asyncio.run(main())
