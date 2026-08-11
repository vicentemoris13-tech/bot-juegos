import asyncio, os
from telegram import Bot
from telegram.error import RetryAfter

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = os.environ.get("CANAL_ID")
AFILIADO = "gamer-a4609b2"
bot = Bot(token=TOKEN)

async def enviar_seguro(texto):
    while True:
        try:
            await bot.send_message(CANAL_ID, text=texto)
            print(f"Enviado: {texto[:20]}")
            return True
        except RetryAfter as e:
            print(f"Telegram me frenó, espero {e.retry_after} seg")
            await asyncio.sleep(e.retry_after + 2)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5)
            return False

async def revisar():
    juegos = ["Red Dead Redemption 2", "Cyberpunk 2077", "Elden Ring", "GTA V", "The Witcher 3"]
    for nombre in juegos:
        link = f"https://www.instant-gaming.com/es/buscar/?q={nombre.replace(' ', '+')}&igr={AFILIADO}"
        msg = f"🔥 {nombre}\n💸 Más barato: {link}"
        await enviar_seguro(msg)
        await asyncio.sleep(7) # 7 segundos entre cada uno para que no te banee

asyncio.run(revisar())
