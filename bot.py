import requests, asyncio, os
from telegram import Bot

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = os.environ.get("CANAL_ID")

bot = Bot(token=TOKEN)

async def revisar():
    try:
        r = requests.get("https://www.gamerpower.com/api/giveaways?platform=epic-games-store&type=game", timeout=15).json()
        juego = r[0]
        msg1 = f"🎮 ¡GRATIS EN EPIC!\n\n{juego['title']}\n\n👉 {juego['open_giveaway']}"
        await bot.send_photo(CANAL_ID, photo=juego['image'], caption=msg1)
    except Exception as e:
        print(f"Error gratis: {e}")

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        data = requests.get("https://store.steampowered.com/api/featuredcategories?cc=cl&l=spanish", headers=headers, timeout=20).json()
        oferta = data['specials']['items'][0]
        msg2 = f"🔥 ¡CHOLLAZO STEAM {oferta['discount_percent']}% OFF!\n\n{oferta['name']}\nAntes ${oferta['original_price']/100} -> Ahora ${oferta['final_price']/100} CLP\n\n👉 https://store.steampowered.com/app/{oferta['id']}/\n\n#Steam #Oferta"
        await bot.send_message(CANAL_ID, text=msg2)
    except Exception as e:
        print(f"Error oferta: {e}")

asyncio.run(revisar())