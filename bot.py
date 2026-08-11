import requests, asyncio, os, time
from telegram import Bot

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = os.environ.get("CANAL_ID")
AFILIADO = "gamer-a4609b2"
bot = Bot(token=TOKEN)

async def revisar():
    # --- 1. 3 OFERTAS STEAM ---
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get("https://store.steampowered.com/api/featuredcategories?cc=cl&l=spanish", headers=headers, timeout=20).json()
        ofertas = r['specials']['items'][:3] # los 3 primeros
        
        for oferta in ofertas:
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
            await asyncio.sleep(3) # espera 3 seg para no ser spam
    except Exception as e:
        print(f"Error steam: {e}")

    # --- 2. 2 JUEGOS GRATIS (Epic + GOG/Steam) ---
    try:
        gratis = requests.get("https://www.gamerpower.com/api/giveaways?sort-by=popularity", timeout=15).json()
        # Filtramos 2 que sean de Epic o Steam
        count = 0
        for juego in gratis:
            if count >= 2: break
            if "Epic" in juego['platforms'] or "Steam" in juego['platforms'] or "DRM" in juego['type']:
                nombre = juego['title'].replace(' ', '+')
                link_ig = f"https://www.instant-gaming.com/es/buscar/?q={nombre}&igr={AFILIADO}"
                
                msg_gratis = (
                    f"🎮 ¡GRATIS! {juego['title']}\n\n"
                    f"Plataforma: {juego['platforms']}\n"
                    f"👉 Reclamar: {juego['open_giveaway_url']}\n\n"
                    f"Si lo quieres sin launcher, en Steam barato: {link_ig}\n\n"
                    f"#Gratis #FreeGame"
                )
                try:
                    await bot.send_photo(CANAL_ID, photo=juego['image'], caption=msg_gratis)
                    count += 1
                    await asyncio.sleep(3)
                except:
                    await bot.send_message(CANAL_ID, text=msg_gratis)
                    count += 1
    except Exception as e:
        print(f"Error gratis: {e}")

asyncio.run(revisar())
