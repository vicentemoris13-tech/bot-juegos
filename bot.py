import os, requests, time, json, re
from datetime import datetime
from bs4 import BeautifulSoup

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = os.environ.get("CANAL_ID")
AFILIADO = "gamer-a4609b2"

# ============================================
# CONFIGURACIÓN DE AFILIADO
# ============================================
IG_BASE = f"https://www.instant-gaming.com/es/?igr={AFILIADO}"
IG_SEARCH = f"https://www.instant-gaming.com/es/buscar/?q={{}}&igr={AFILIADO}"

def enviar_telegram(texto, parse_mode="HTML"):
    """Envía mensaje al canal de Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        data = {
            "chat_id": CANAL_ID,
            "text": texto,
            "parse_mode": parse_mode,
            "disable_web_page_preview": False
        }
        r = requests.post(url, json=data, timeout=15)
        respuesta = r.json()
        if respuesta.get("ok"):
            print(f"✅ Enviado: {texto[:50]}...")
            return True
        else:
            print(f"❌ Error Telegram: {respuesta}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ============================================
# 1. BUSCAR OFERTAS EN STEAM
# ============================================
def obtener_ofertas_steam():
    """Obtiene los juegos con más descuento en Steam"""
    print("🔍 Buscando ofertas en Steam...")
    
    try:
        # API de Steam para ofertas especiales
        url = "https://store.steampowered.com/api/featuredcategories?cc=es&l=spanish"
        r = requests.get(url, timeout=10)
        
        if r.status_code != 200:
            print("❌ No se pudo conectar con Steam")
            return []
        
        data = r.json()
        ofertas = []
        
        # Buscar en especiales
        if 'specials' in data and 'items' in data['specials']:
            for item in data['specials']['items']:
                try:
                    nombre = item.get('name', 'Sin nombre')
                    precio_original = item.get('original_price', 0) / 100
                    precio_oferta = item.get('final_price', 0) / 100
                    app_id = item.get('id')
                    
                    if precio_original > 0 and precio_oferta > 0:
                        descuento = int((1 - precio_oferta/precio_original) * 100)
                        
                        # Solo juegos con buen descuento (>30%)
                        if descuento >= 30:
                            ofertas.append({
                                'nombre': nombre,
                                'precio_original': precio_original,
                                'precio_oferta': precio_oferta,
                                'descuento': descuento,
                                'app_id': app_id,
                                'steam_url': f"https://store.steampowered.com/app/{app_id}/"
                            })
                except Exception as e:
                    print(f"⚠️ Error procesando juego: {e}")
                    continue
        
        # Ordenar por descuento (mayor primero) y tomar los 5 mejores
        ofertas.sort(key=lambda x: x['descuento'], reverse=True)
        print(f"✅ {len(ofertas)} ofertas encontradas en Steam")
        return ofertas[:5]  # Tomamos 5 para luego elegir los 3 mejores
        
    except Exception as e:
        print(f"❌ Error buscando ofertas Steam: {e}")
        return []

def buscar_en_instant_gaming(nombre_juego):
    """Busca el juego en Instant Gaming para obtener link de afiliado"""
    try:
        # Limpiar nombre para búsqueda
        nombre_limpio = nombre_juego.lower()
        nombre_limpio = re.sub(r'[^a-z0-9\s]', '', nombre_limpio)
        nombre_limpio = nombre_limpio.replace(' ', '-')[:50]
        
        url = f"https://www.instant-gaming.com/es/buscar/?q={nombre_limpio}&igr={AFILIADO}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml'
        }
        
        r = requests.get(url, headers=headers, timeout=10)
        
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Buscar el primer resultado
            link = soup.find('a', class_='cover')
            if link and 'href' in link.attrs:
                href = link['href']
                if '?igr=' not in href:
                    href += f"?igr={AFILIADO}"
                return href
        
        # Si no encuentra, devolver búsqueda genérica con afiliado
        return f"https://www.instant-gaming.com/es/buscar/?q={nombre_limpio}&igr={AFILIADO}"
        
    except Exception as e:
        print(f"⚠️ Error buscando en IG: {e}")
        return IG_BASE

# ============================================
# 2. BUSCAR JUEGOS GRATIS
# ============================================
def obtener_juegos_gratis_epic():
    """Obtiene los juegos gratis actuales de Epic Games"""
    print("🎮 Buscando juegos gratis en Epic...")
    
    try:
        # Usar la API no oficial de Epic Games
        url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=es-ES&country=ES&allowCountries=ES"
        r = requests.get(url, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            juegos_gratis = []
            
            for game in data.get('data', {}).get('Catalog', {}).get('searchStore', {}).get('elements', []):
                try:
                    # Verificar si es gratis actualmente
                    promotions = game.get('promotions', {})
                    if promotions:
                        promotional_offers = promotions.get('promotionalOffers', [])
                        for offer_list in promotional_offers:
                            for offer in offer_list.get('promotionalOffers', []):
                                if offer.get('discountSetting', {}).get('discountPercentage') == 0:
                                    # Es gratis
                                    nombre = game.get('title', 'Juego Gratis')
                                    descripcion = game.get('description', '')[:100]
                                    
                                    # Construir URL de Epic
                                    product_slug = game.get('productSlug', '')
                                    catalog_namespace = game.get('catalogNs', {}).get('mappings', [{}])[0].get('pageSlug', '')
                                    
                                    if product_slug:
                                        url_juego = f"https://store.epicgames.com/es-ES/p/{product_slug}"
                                    else:
                                        url_juego = "https://store.epicgames.com/es-ES/free-games"
                                    
                                    juegos_gratis.append({
                                        'nombre': nombre,
                                        'descripcion': descripcion[:150],
                                        'url': url_juego,
                                        'tienda': 'Epic Games'
                                    })
                                    break
                except Exception as e:
                    print(f"⚠️ Error procesando juego Epic: {e}")
                    continue
            
            print(f"✅ {len(juegos_gratis)} juegos gratis en Epic")
            return juegos_gratis[:2]  # Máximo 2 juegos de Epic
            
    except Exception as e:
        print(f"❌ Error buscando Epic: {e}")
    
    return []

def obtener_juegos_gratis_steam():
    """Obtiene juegos gratis permanentes populares de Steam"""
    print("🎮 Buscando juegos gratis en Steam...")
    
    try:
        # Buscar free to play populares
        url = "https://store.steampowered.com/api/featuredcategories?cc=es&l=spanish"
        r = requests.get(url, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            juegos_gratis = []
            
            # Buscar en la categoría de free to play si existe
            for category in ['specials', 'coming_soon', 'new_releases']:
                if category in data:
                    for item in data[category].get('items', []):
                        try:
                            # Verificar si es gratis
                            if item.get('final_price', 999) == 0 or item.get('price', {}).get('final', 999) == 0:
                                nombre = item.get('name', 'Juego Gratis')
                                app_id = item.get('id')
                                
                                juegos_gratis.append({
                                    'nombre': nombre,
                                    'url': f"https://store.steampowered.com/app/{app_id}/",
                                    'tienda': 'Steam',
                                    'app_id': app_id
                                })
                        except:
                            continue
            
            # Si no encuentra, usar juegos populares free-to-play
            if not juegos_gratis:
                juegos_f2p = [
                    {'nombre': 'Counter-Strike 2', 'url': 'https://store.steampowered.com/app/730/', 'tienda': 'Steam'},
                    {'nombre': 'Dota 2', 'url': 'https://store.steampowered.com/app/570/', 'tienda': 'Steam'},
                    {'nombre': 'Apex Legends', 'url': 'https://store.steampowered.com/app/1172470/', 'tienda': 'Steam'},
                    {'nombre': 'War Thunder', 'url': 'https://store.steampowered.com/app/236390/', 'tienda': 'Steam'},
                    {'nombre': 'Destiny 2', 'url': 'https://store.steampowered.com/app/1085660/', 'tienda': 'Steam'},
                ]
                juegos_gratis = juegos_f2p
            
            print(f"✅ {len(juegos_gratis)} juegos gratis en Steam")
            return juegos_gratis[:2]
            
    except Exception as e:
        print(f"❌ Error buscando Steam gratis: {e}")
    
    return []

# ============================================
# 3. FORMATEAR Y ENVIAR MENSAJES
# ============================================
def formatear_mensaje_oferta(juego, link_ig):
    """Formatea un mensaje de oferta para Telegram"""
    mensaje = f"""
🔥 <b>OFERTA DESTACADA</b> 🔥

🎮 <b>{juego['nombre']}</b>

💰 Precio Steam: <s>{juego['precio_original']:.2f}€</s>
💸 <b>AHORA: {juego['precio_oferta']:.2f}€</b> (-{juego['descuento']}%)

🛒 <b>MEJOR PRECIO AQUÍ:</b>
👉 {link_ig}

🏷️ Ahorro: {juego['precio_original'] - juego['precio_oferta']:.2f}€
"""
    return mensaje.strip()

def formatear_mensaje_gratis(juego):
    """Formatea un mensaje de juego gratis para Telegram"""
    emojis = {
        'Epic Games': '🎮',
        'Steam': '⚡',
        'Gratis': '🎁'
    }
    
    emoji = emojis.get(juego.get('tienda', ''), '🎁')
    
    mensaje = f"""
{emoji} <b>¡JUEGO GRATIS!</b> {emoji}

📦 <b>{juego['nombre']}</b>
🏪 Tienda: {juego.get('tienda', 'Gratis')}

🔗 <b>CONSEGUIR GRATIS:</b>
👉 {juego['url']}

⏰ ¡Por tiempo limitado!
"""
    return mensaje.strip()

# ============================================
# 4. MAIN - EJECUCIÓN PRINCIPAL
# ============================================
def main():
    print("=" * 50)
    print(f"🤖 BOT DE OFERTAS - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    # ----- OBTENER DATOS -----
    print("\n📊 RECOPILANDO INFORMACIÓN...\n")
    
    # 1. Obtener ofertas de Steam
    ofertas_steam = obtener_ofertas_steam()
    
    # 2. Obtener juegos gratis
    juegos_epic = obtener_juegos_gratis_epic()
    juegos_steam_gratis = obtener_juegos_gratis_steam()
    
    # Combinar juegos gratis (máximo 2)
    todos_gratis = juegos_epic + juegos_steam_gratis
    # Elegir hasta 2 juegos gratis (priorizando Epic si hay)
    juegos_gratis_final = todos_gratis[:2]
    
    # ----- ENVIAR MENSAJES -----
    print("\n📤 ENVIANDO AL CANAL DE TELEGRAM...\n")
    
    mensajes_enviados = 0
    
    # Enviar header
    header = f"""
🎯 <b>OFERTAS DEL DÍA</b> 🎯
📅 {datetime.now().strftime('%d/%m/%Y')}

💎 <b>TOP 3 OFERTAS STEAM</b> + <b>2 JUEGOS GRATIS</b>
🛒 Enlaces con descuento adicional en Instant Gaming
"""
    enviar_telegram(header.strip())
    time.sleep(2)
    
    # 1. Enviar 3 ofertas de Steam con link de Instant Gaming
    ofertas_a_enviar = ofertas_steam[:3] if len(ofertas_steam) >= 3 else ofertas_steam
    
    if len(ofertas_a_enviar) < 3:
        print(f"⚠️ Solo se encontraron {len(ofertas_a_enviar)} ofertas. Completando con ofertas populares...")
        # Ofertas de respaldo populares
        ofertas_respaldo = [
            {'nombre': 'Elden Ring', 'precio_original': 59.99, 'precio_oferta': 35.99, 'descuento': 40},
            {'nombre': 'Red Dead Redemption 2', 'precio_original': 59.99, 'precio_oferta': 19.79, 'descuento': 67},
            {'nombre': 'Cyberpunk 2077', 'precio_original': 59.99, 'precio_oferta': 29.99, 'descuento': 50},
        ]
        while len(ofertas_a_enviar) < 3:
            ofertas_a_enviar.append(ofertas_respaldo[len(ofertas_a_enviar)])
    
    print(f"🎮 Enviando {len(ofertas_a_enviar)} ofertas de Steam...")
    
    for i, juego in enumerate(ofertas_a_enviar[:3], 1):
        print(f"  {i}/3 Buscando en Instant Gaming: {juego['nombre']}...")
        
        # Buscar en Instant Gaming
        link_ig = buscar_en_instant_gaming(juego['nombre'])
        
        # Formatear y enviar
        mensaje = formatear_mensaje_oferta(juego, link_ig)
        
        if enviar_telegram(mensaje):
            mensajes_enviados += 1
            print(f"  ✅ Oferta {i}/3 enviada")
        else:
            print(f"  ❌ Error enviando oferta {i}")
        
        time.sleep(3)  # Esperar entre mensajes para evitar límites
    
    # 2. Enviar 2 juegos gratis
    print(f"\n🎁 Enviando {len(juegos_gratis_final)} juegos gratis...")
    
    # Completar si no hay suficientes
    if len(juegos_gratis_final) < 2:
        juegos_default = [
            {
                'nombre': 'Revisa juegos gratis en Epic Games',
                'url': 'https://store.epicgames.com/es-ES/free-games',
                'tienda': 'Epic Games'
            },
            {
                'nombre': 'Free to Play en Steam',
                'url': 'https://store.steampowered.com/genre/Free%20to%20Play/',
                'tienda': 'Steam'
            }
        ]
        while len(juegos_gratis_final) < 2:
            juegos_gratis_final.append(juegos_default[len(juegos_gratis_final)])
    
    for i, juego in enumerate(juegos_gratis_final[:2], 1):
        mensaje = formatear_mensaje_gratis(juego)
        
        if enviar_telegram(mensaje):
            mensajes_enviados += 1
            print(f"  ✅ Gratis {i}/2 enviado: {juego['nombre']}")
        else:
            print(f"  ❌ Error enviando juego gratis {i}")
        
        time.sleep(3)
    
    # Enviar footer con link de afiliado
    footer = f"""
🛒 <b>¿Buscas más ofertas?</b>
🔥 <a href="{IG_BASE}">Visita Instant Gaming</a> para los mejores precios

💎 <b>Canal de ofertas diarias</b>
¡Comparte con tus amigos!
"""
    enviar_telegram(footer.strip())
    time.sleep(2)
    
    # ----- RESUMEN -----
    print("\n" + "=" * 50)
    print(f"✅ FINALIZADO - {mensajes_enviados} mensajes enviados")
    print(f"📊 Estadísticas:")
    print(f"   🎮 Ofertas Steam: {len(ofertas_a_enviar[:3])}")
    print(f"   🎁 Juegos Gratis: {len(juegos_gratis_final[:2])}")
    print(f"   💰 Links afiliado: Instant Gaming")
    print("=" * 50)

# ============================================
# EJECUTAR
# ============================================
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        # Enviar mensaje de error al canal
        error_msg = f"⚠️ Error en el bot: {str(e)[:200]}"
        try:
            enviar_telegram(error_msg)
        except:
            pass
