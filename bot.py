import requests, asyncio, os
from telegram import Bot

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = os.environ.get("CANAL_ID")
AFILIADO = "link_ig = f"https://www.instant-gaming.com/?igr={AFILIADO}" # tu codigo

bot = Bot(token=TOKEN)

async def revisar():
    # --- STEAM ---
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get("https://store.steampowered.com/api/featuredcategories?cc=cl&l=spanish", headers=headers, timeout=20).json()
        oferta = r['specials']['items'][0]

        nombre_busqueda = oferta['name'].replace(' ', '+')
        link_ig = f"https://www.instant-gaming.com/es/buscar/?q={nombre_busqueda}&igr={AFILIADO}"

        msg = (
            f"🔥 ¡CHOLLAZO STEAM {oferta['discount_percent']}% OFF!\n\n"
            f"{oferta['name']}\n"
            f"Antes ${oferta['original_price']/100} -> Ahora ${oferta['final_price']/100} CLP\n\n"
            f"👉 Steam: https://store.steampowered.com/app/{oferta['id']}/\n"
            f"💸 Más barato en Instant: {link_ig}\n\n"
            f"#Steam #Oferta #Chile"
        )
        await bot.send_message(CANAL_ID, text=msg)

    except Exception as e:
        print(f"Error steam: {e}")

    # --- EPIC GRATIS (si hay) ---
    try:
        epic = requests.get("https://www.gamerpower.com/api/giveaways?platform=epic-games-store&type=game", timeout=15).json()
        if epic:
            juego = epic[0]
            # Busca ese juego gratis en Instant para comparar (aunque sea gratis en Epic)
            link_ig_epic = f"https://www.instant-gaming.com/es/buscar/?q={juego['title'].replace(' ', '+')}&igr={AFILIADO}"
            msg_epic = f"🎮 ¡GRATIS EN EPIC!\n\n{juego['title']}\n\n👉 {juego['open_giveaway']}\n\nSi lo quieres para Steam más barato: {link_ig_epic}"
            await bot.send_photo(CANAL_ID, photo=juego['image'], caption=msg_epic)
    except Exception as e:
        print(f"Error epic: {e}")

asyncio.run(revisar())
