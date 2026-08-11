import os, requests, time, json
from datetime import datetime

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = os.environ.get("CANAL_ID")
AFILIADO = "gamer-a4609b2"

def enviar_telegram(texto, parse_mode=None):
    """Función simple para enviar mensajes"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CANAL_ID, "text": texto}
    if parse_mode:
        data["parse_mode"] = parse_mode
    
    try:
        r = requests.post(url, data=data, timeout=15)
        respuesta = r.json()
        if respuesta.get("ok"):
            print(f"✅ Enviado: {texto[:50]}...")
            return True
        else:
            print(f"❌ Error: {respuesta.get('description')}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def obtener_ofertas_steam():
    """Busca ofertas reales en Steam"""
    ofertas = []
    try:
        print("🔍 Buscando en Steam API...")
        url = "https://store.steampowered.com/api/featuredcategories?cc=es&l=spanish"
        r = requests.get(url, timeout=10)
        
        if r.status_code != 200:
            print(f"Error HTTP: {r.status_code}")
            return None
            
        data = r.json()
        
        if 'specials' not in data:
            print("No hay 'specials' en la respuesta")
            return None
            
        items = data['specials'].get('items', [])
        print(f"Encontrados {len(items)} items")
        
        for item in items[:5]:
            try:
                nombre = item.get('name', 'Sin nombre')
                precio_original = item.get('original_price', 0)
                precio_final = item.get('final_price', 0)
                
                if precio_original and precio_final and precio_original > 0:
                    precio_original = precio_original / 100
                    precio_final = precio_final / 100
                    descuento = int((1 - precio_final/precio_original) * 100)
                    
                    if descuento >= 20:
                        ofertas.append({
                            'nombre': nombre,
                            'precio_original': precio_original,
                            'precio_final': precio_final,
                            'descuento': descuento
                        })
                        print(f"  ✅ {nombre}: -{descuento}%")
            except Exception as e:
                print(f"  ⚠️ Error item: {e}")
                continue
                
    except Exception as e:
        print(f"❌ Error Steam: {e}")
        return None
    
    if ofertas:
        ofertas.sort(key=lambda x: x['descuento'], reverse=True)
        return ofertas[:3]
    return None

def main():
    print("=" * 50)
    print(f"🤖 BOT INICIADO - {datetime.now()}")
    print("=" * 50)
    
    # Verificar configuración
    if not TOKEN or not CANAL_ID:
        print("❌ ERROR: Token o Canal no configurados")
        print(f"TOKEN: {'Configurado' if TOKEN else 'FALTA'}")
        print(f"CANAL_ID: {'Configurado' if CANAL_ID else 'FALTA'}")
        return
    
    # 1. Intentar obtener ofertas reales
    ofertas = obtener_ofertas_steam()
    
    # 2. Si falla, usar ofertas de respaldo
    if not ofertas:
        print("⚠️ Usando ofertas de respaldo")
        ofertas = [
            {'nombre': 'Elden Ring', 'precio_original': 59.99, 'precio_final': 35.99, 'descuento': 40},
            {'nombre': 'GTA V', 'precio_original': 29.99, 'precio_final': 14.99, 'descuento': 50},
            {'nombre': 'Cyberpunk 2077', 'precio_original': 59.99, 'precio_final': 29.99, 'descuento': 50}
        ]
    
    # 3. Enviar header
    header = f"🎯 OFERTAS DEL DÍA - {datetime.now().strftime('%d/%m/%Y')}\n\n🔥 TOP 3 OFERTAS + 2 JUEGOS GRATIS"
    enviar_telegram(header)
    time.sleep(2)
    
    # 4. Enviar 3 ofertas
    print(f"\n📤 Enviando {len(ofertas[:3])} ofertas...")
    for i, oferta in enumerate(ofertas[:3], 1):
        link_ig = f"https://www.instant-gaming.com/es/?igr={AFILIADO}"
        
        mensaje = (
            f"🎮 OFERTA #{i}\n\n"
            f"📦 {oferta['nombre']}\n"
            f"💰 Precio: {oferta['precio_original']:.2f}€\n"
            f"💸 AHORA: {oferta['precio_final']:.2f}€ (-{oferta['descuento']}%)\n\n"
            f"🛒 COMPRAR: {link_ig}"
        )
        
        if enviar_telegram(mensaje):
            print(f"  ✅ Oferta {i}/3")
        else:
            print(f"  ❌ Oferta {i}/3")
        time.sleep(3)
    
    # 5. Enviar 2 juegos gratis
    print(f"\n📤 Enviando juegos gratis...")
    
    juegos_gratis = [
        {
            'nombre': 'Juegos Gratis Epic Games',
            'url': 'https://store.epicgames.com/es-ES/free-games',
            'tienda': 'Epic Games'
        },
        {
            'nombre': 'Free to Play Steam',
            'url': 'https://store.steampowered.com/genre/Free%20to%20Play/',
            'tienda': 'Steam'
        }
    ]
    
    for i, juego in enumerate(juegos_gratis, 1):
        mensaje = (
            f"🎁 JUEGO GRATIS #{i}\n\n"
            f"📦 {juego['nombre']}\n"
            f"🏪 {juego['tienda']}\n\n"
            f"🔗 CONSEGUIR: {juego['url']}"
        )
        
        if enviar_telegram(mensaje):
            print(f"  ✅ Gratis {i}/2")
        else:
            print(f"  ❌ Gratis {i}/2")
        time.sleep(3)
    
    # 6. Footer
    footer = f"🛒 Más ofertas: https://www.instant-gaming.com/es/?igr={AFILIADO}"
    enviar_telegram(footer)
    
    print("\n" + "=" * 50)
    print("✅ FIN - Revisa tu canal de Telegram")
    print("=" * 50)

if __name__ == "__main__":
    main()
