import requests, asyncio, os
from telegram import Bot
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = os.environ.get("CANAL_ID")
bot = Bot(token=TOKEN)
async def revisar():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get("https://store.steampowered.com/api/featuredcategories?cc=cl&l=spanish", headers=headers, timeout=20).json()
        oferta = r['specials']['items'][0]
        msg = (
            f"🔥 ¡CHOLLAZO STEAM {oferta['discount_percent']}% OFF!\n\n"
            f"{oferta['name']}\n"
            f"Antes ${oferta['original_price']/100} -> Ahora ${oferta['final_price']/100} CLP\n\n"
            f"👉 Steam: https://store.steampowered.com/app/{oferta['id']}/\n"
            f"💸 Más barato: https://www.instant-gaming.com/?igr=gamer-a4609b2\n\n"
            f"#Steam #Oferta #Chile"
        )
        await bot.send_message(CANAL_ID, text=msg)
    except Exception as e:
        print(f"Error: {e}")
asyncio.run(revisar())
