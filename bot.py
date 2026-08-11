import requests, asyncio, os
from telegram import Bot

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = os.environ.get("CANAL_ID")
AFILIADO = "gamer-a4609b2"
bot = Bot(token=TOKEN)

async def revisar():
    # --- 3 OFERTAS STEAM ---
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get("https://store.steampowered.com/api/featuredcategories?cc=cl&l=spanish", headers=headers, timeout=20).json()
        ofertas = r['specials']['items'][:3]
        
        for oferta in ofertas:
            try:
                nombre = oferta['name'].replace(' ', '+')
                link_ig = f"https://www.instant-gaming.com/es/buscar/?q={nombre}&igr={AFILIADO}"
                msg = (
                    f"🔥 ¡CHOLLAZO {oferta['discount_percent']}% OFF!\n\n"
                    f"{oferta['name']}\n"
                    f"Antes ${oferta['original_price']/100} -> Ahora ${oferta['final_price']/100} CLP\n\n"
                    f"👉 Steam: https://store.steampowered.com/app/{oferta['id']}/\n"
                    f"💸 Más barato: {link_ig}\n\n"
                    f"#Steam #Oferta #Chile"
                )
                await bot.send_message(CANAL_ID, text=msg)
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Error en juego {oferta['name']}: {e}")
                continue
    except Exception as e:
        print(f"Error steam general: {e}")

    # --- 2 GRATIS ---
    try:
        gratis = requests.get("https://www.gamerpower.com/api/giveaways", timeout=15).json()
        enviados = 0
        for juego in gratis:
            if enviados >= 2: break
            try:
                nombre = juego['title'].replace(' ', '+')
                link_ig = f"https://www.instant-gaming.com/es/buscar/?q={nombre}&igr={AFILIADO}"
                msg_gratis = (
                    f"🎮 ¡GRATIS! {juego['title']}\n"
                    f"👉 {juego['open_giveaway_url']}\n\n"
                    f"Si lo quieres en Steam barato: {link_ig}\n\n"
                    f"#Gratis"
                )
                await bot.send_photo(CANAL_ID, photo=juego['image'], caption=msg_gratis)
                enviados += 1
                await asyncio.sleep(5)
            except:
                continue
    except Exception as e:
        print(f"Error gratis: {e}")

asyncio.run(revisar())
