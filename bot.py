import requests, asyncio, os
from telegram import Bot

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = os.environ.get("CANAL_ID")
AFILIADO = "gamer-a4609b2"
bot = Bot(token=TOKEN)

async def revisar():
    # --- 3 JUEGOS BARATOS - API que no falla ---
    try:
        # CheapShark = ofertas reales de Steam
        r = requests.get("https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15&sortBy=Savings&onSale=1&pageSize=3", timeout=20).json()
        for oferta in r:
            try:
                nombre = oferta['title'].replace(' ', '+')
                link_ig = f"https://www.instant-gaming.com/es/buscar/?q={nombre}&igr={AFILIADO}"
                ahorro = int(float(oferta['savings']))
                msg = (
                    f"🔥 ¡CHOLLAZO {ahorro}% OFF!\n\n"
                    f"{oferta['title']}\n"
                    f"Antes ${oferta['normalPrice']} -> Ahora ${oferta['salePrice']} USD\n\n"
                    f"👉 Ver en Steam: https://store.steampowered.com/app/{oferta['steamAppID']}/\n"
                    f"💸 Más barato: {link_ig}\n\n"
                    f"#Steam #Oferta"
                )
                await bot.send_message(CANAL_ID, text=msg)
                await asyncio.sleep(4)
            except Exception as e:
                print(e)
                continue
    except Exception as e:
        print(f"Error ofertas: {e}")

    # --- 2 GRATIS - Epic directo ---
    try:
        r = requests.get("https://store-site-backend-static.ak.epicgames.com/freeGamesPromos?locale=es-ES&country=CL", timeout=20).json()
        juegos = r['data']['Catalog']['searchStore']['elements']
        count = 0
        for j in juegos:
            if count >= 2: break
            if j['promotions'] and j['promotions']['promotionalOffers']:
                titulo = j['title']
                link_ig = f"https://www.instant-gaming.com/es/buscar/?q={titulo.replace(' ', '+')}&igr={AFILIADO}"
                msg = (
                    f"🎮 ¡GRATIS EN EPIC! {titulo}\n\n"
                    f"👉 Reclamar en Epic Games Store\n"
                    f"💸 Versión Steam barata: {link_ig}\n\n"
                    f"#Gratis #Epic"
                )
                if j['keyImages']:
                    img = j['keyImages'][0]['url']
                    await bot.send_photo(CANAL_ID, photo=img, caption=msg)
                else:
                    await bot.send_message(CANAL_ID, text=msg)
                count += 1
                await asyncio.sleep(4)
    except Exception as e:
        print(f"Error epic: {e}")

asyncio.run(revisar())
