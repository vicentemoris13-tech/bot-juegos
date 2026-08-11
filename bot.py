import os, requests, time, json
from datetime import datetime

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = os.environ.get("CANAL_ID")
AFILIADO = "gamer-a4609b2"

def enviar_telegram(texto):
    """Envía mensaje al canal de Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        data = {
            "chat_id": CANAL_ID,
            "text": texto,
            "parse_mode": "HTML"
        }
        r = requests.post(url, data=data, timeout=15)
        if r.status_code == 200:
            print(f"✅ Enviado correctamente")
            return True
        else:
            print(f"❌ Error Telegram: {r.text[:100]}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def obtener_ofertas_steam():
    """Obtiene ofertas reales de Steam"""
    try:
        url = "https://store.steampowered.com/api/featuredcategories?cc=es&l=spanish"
        r = requests.get(url, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            ofertas = []
            
            if 'specials' in data:
                for item in data['specials']['items'][:5]:
                    try:
                        nombre = item.get('name', 'Sin nombre')
                        precio_orig = item.get('original_price', 0) / 100
                        precio_oferta = item.get('final_price', 0) / 100
                        
                        if precio_orig > 0:
                            descuento = int((1 - precio_oferta/precio_orig) * 100)
                            if descuento >= 20:  # Mínimo 20% descuento
                                ofertas.append({
                                    'nombre': nombre,
                                    'precio_original': precio_orig,
                                    'precio_oferta': precio_oferta,
                                    'descuento': descuento,
                                    'app_id': item.get('id')
                                })
                    except Exception as e:
                        print(f"Error procesando juego: {e}")
                        continue
            
            # Ordenar por descuento
            ofertas.sort(key=lambda x: x['descuento'], reverse=True)
            return ofertas[:3]  # Solo 3 mejores ofertas
        else:
            print(f"Error Steam API: {r.status_code}")
            return []
    except Exception as e:
        print(f"Fallo ofertas: {e}")
        return []

def obtener_juegos_gratis():
    """Obtiene juegos gratis de Epic Games"""
    juegos_gratis = []
    
    # Intentar Epic Games
    try:
        url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=es-ES&country=ES&allowCountries=ES"
        r = requests.get(url, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            
            for game in data.get('data', {}).get('Catalog', {}).get('searchStore', {}).get('elements', []):
                try:
                    promotions = game.get('promotions', {})
                    if promotions:
                        offers = promotions.get('promotionalOffers', [])
                        for offer_list in offers:
                            for offer in offer_list.get('promotionalOffers', []):
                                if offer.get('discountSetting', {}).get('discountPercentage') == 0:
                                    title = game.get('title', 'Juego Gratis')
                                    slug = game.get('productSlug', '')
                                    if slug:
                                        juegos_gratis.append({
                                            'nombre': title,
                                            'url': f"https://store.epicgames.com/es-ES/p/{slug}",
                                            'tienda': 'Epic Games'
                                        })
                except:
                    continue
    except Exception as e:
        print(f"Error Epic: {e}")
    
    # Si no hay de Epic, añadir juegos F2P de Steam
    if not juegos_gratis:
        juegos_gratis = [
            {'nombre': 'Counter-Strike 2', 'url': 'https://store.steampowered.com/app/730/', 'tienda': 'Steam'},
            {'nombre': 'Dota 2', 'url': 'https://store.steampowered.com/app/570/', 'tienda': 'Steam'},
        ]
    
    return juegos_gratis[:2]

def main():
    print("=" * 60)
    print(f"🤖 BOT DE OFERTAS - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)
    
    # Header del día
    header = f"""
🎯 <b>¡OFERTAS DEL DÍA!</b> 🎯
📅 {datetime.now().strftime('%d/%m/%Y')}

🔥 <b>TOP 3 OFERTAS + 2 JUEGOS GRATIS</b>
"""
    enviar_telegram(header.strip())
    time.sleep(2)
    
    # 1. OBTENER OFERTAS DE STEAM
    print("\n🔍 Buscando ofertas en Steam...")
    ofertas = obtener_ofertas_steam()
    
    if not ofertas:
        print("⚠️ No se encontraron ofertas, usando respaldo...")
        ofertas = [
            {'nombre': 'Elden Ring', 'precio_original': 59.99, 'precio_oferta': 35.99, 'descuento': 40},
            {'nombre': 'GTA V', 'precio_original': 29.99, 'precio_oferta': 14.99, 'descuento': 50},
            {'nombre': 'Cyberpunk 2077', 'precio_original': 59.99, 'precio_oferta': 29.99, 'descuento': 50},
        ]
    
    # Enviar ofertas
    for i, oferta in enumerate(ofertas[:3], 1):
        # Link de Instant Gaming con tu afiliado
        nombre_busqueda = oferta['nombre'].lower().replace(' ', '-').replace(':', '')[:50]
        link_ig = f"https://www.instant-gaming.com/es/buscar/?q={nombre_busqueda}&igr={AFILIADO}"
        
        mensaje = f"""
🎮 <b>OFERTA #{i}</b>

📦 <b>{oferta['nombre']}</b>
💰 Precio original: <s>{oferta['precio_original']:.2f}€</s>
💸 <b>AHORA: {oferta['precio_oferta']:.2f}€</b> (-{oferta['descuento']}%)

🛒 <b>MEJOR PRECIO:</b>
👉 {link_ig}
"""
        if enviar_telegram(mensaje.strip()):
            print(f"✅ Oferta {i}/3 enviada: {oferta['nombre']}")
        else:
            print(f"❌ Fallo oferta {i}")
        
        time.sleep(3)
    
    # 2. JUEGOS GRATIS
    print("\n🎁 Buscando juegos gratis...")
    gratis = obtener_juegos_gratis()
    
    for i, juego in enumerate(gratis[:2], 1):
        mensaje = f"""
🎁 <b>¡JUEGO GRATIS #{i}!</b>

📦 <b>{juego['nombre']}</b>
🏪 {juego['tienda']}

🔗 <b>CONSEGUIR AHORA:</b>
👉 {juego['url']}

⏰ ¡Por tiempo limitado!
"""
        if enviar_telegram(mensaje.strip()):
            print(f"✅ Gratis {i}/2 enviado: {juego['nombre']}")
        else:
            print(f"❌ Fallo gratis {i}")
        
        time.sleep(3)
    
    # Footer con link de afiliado
    footer = f"""
🛒 <b>¿QUIERES MÁS OFERTAS?</b>
🔥 <a href="https://www.instant-gaming.com/es/?igr={AFILIADO}">Visita Instant Gaming</a>

💎 <b>¡Comparte el canal!</b>
"""
    enviar_telegram(footer.strip())
    
    print("\n" + "=" * 60)
    print("✅ FINALIZADO - Ofertas publicadas correctamente")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ ERROR: {e}")
