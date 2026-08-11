import asyncio, os
from telegram import Bot
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = os.environ.get("CANAL_ID")
AFILIADO = "gamer-a4609b2"
bot = Bot(token=TOKEN)
async def revisar():
    for nombre in ["Juego 1","Juego 2","Juego 3","Juego 4","Juego 5"]:
        link = f"https://www.instant-gaming.com/es/buscar/?q={nombre}&igr={AFILIADO}"
        await bot.send_message(CANAL_ID, text=f"TEST {nombre} -> {link}")
        await asyncio.sleep(2)
asyncio.run(revisar())
