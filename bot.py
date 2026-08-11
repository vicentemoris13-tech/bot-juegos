import requests, asyncio, os
from telegram import Bot
import time

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = os.environ.get("CANAL_ID")
AFILIADO = "gamer-a4609b2"
bot = Bot(token=TOKEN)

print(f"INICIANDO BOT - CANAL {CANAL_ID}")

async def revisar():
    # 3 ofertas
    try:
        r = requests.get("https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=20&sortBy=Savings&onSale=1&pageSize=3", timeout=20).json()
        print(f"Ofertas encontradas: {len(r)}")
        for oferta in r:
            nombre = oferta['title']
            link_ig = f"https://www.instant-gaming.com/es/buscar/?q={nombre.replace(' ', '+')}&igr={AFILIADO}"
            msg = f"🔥 {nombre} {int(float(oferta['savings']))}% OFF\nAntes ${oferta['normalPrice']} -> Ahora ${oferta['salePrice']} USD\n👉 https://store.steampowered.com/app/{oferta['steamAppID']}/\n💸 Más barato: {link_ig}"
            await bot.send_message(CANAL_ID, text=msg)
            print(f"Enviado: {nombre}")
            await asyncio.sleep(5)
    except Exception as e:
        print(f"Error ofertas: {e}")

    # 2 gratis Epic
    try:
        r = requests.get("https://store-site-backend-static.ak.epicgames.com/freeGamesPromos?locale=es-ES&country=CL", timeout=20).json()
        juegos = r['data']['Catalog']['searchStore']['elements']
        count=0
        for j in juegos:
            if count>=2: break
            if j.get('promotions') and j['promotions']['promotionalOffers']:
                titulo=j['title']
                link_ig=f"https://www.instant-gaming.com/es/buscar/?q={titulo.replace(' ', '+')}&igr={AFILIADO}"
                msg=f"🎮 ¡GRATIS! {titulo}\n💸 Versión Steam barata: {link_ig}"
                try:
                    await bot.send_photo(CANAL_ID, photo=j['keyImages'][0]['url'], caption=msg)
                except:
                    await bot.send_message(CANAL_ID, text=msg)
                print(f"Gratis enviado: {titulo}")
                count+=1
                await asyncio.sleep(5)
    except Exception as e:
        print(f"Error epic: {e}")

asyncio.run(revisar())
print("FIN")
