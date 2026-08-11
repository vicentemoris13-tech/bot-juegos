import os, requests, time
from datetime import datetime

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = os.environ.get("CANAL_ID")
AFILIADO = "gamer-a4609b2"

print("=" * 60)
print("🔍 DIAGNÓSTICO DEL BOT")
print("=" * 60)

# 1. Verificar variables de entorno
print(f"\n1️⃣ Verificando configuración:")
print(f"   Token: {TOKEN[:10]}...{TOKEN[-5:] if TOKEN and len(TOKEN) > 15 else 'NO ENCONTRADO'}")
print(f"   Canal ID: {CANAL_ID if CANAL_ID else 'NO ENCONTRADO'}")
print(f"   Afiliado: {AFILIADO}")

if not TOKEN:
    print("❌ ERROR: Token no configurado")
    exit(1)
if not CANAL_ID:
    print("❌ ERROR: Canal ID no configurado")
    exit(1)

# 2. Probar conexión básica con Telegram
print(f"\n2️⃣ Probando conexión con Telegram...")
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# Mensaje de prueba simple
test_message = f"🧪 Test del bot - {datetime.now().strftime('%H:%M:%S')}"

try:
    response = requests.post(
        url,
        data={
            "chat_id": CANAL_ID,
            "text": test_message
        },
        timeout=15
    )
    
    print(f"   Status: {response.status_code}")
    print(f"   Respuesta: {response.text[:200]}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("ok"):
            print("✅ Conexión exitosa con Telegram")
            message_id = data.get('result', {}).get('message_id')
            print(f"   Mensaje ID: {message_id}")
        else:
            print(f"❌ Error Telegram: {data.get('description')}")
    else:
        print(f"❌ Error HTTP: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error de conexión: {e}")

# 3. Probar mensaje con HTML
print(f"\n3️⃣ Probando mensaje con formato HTML...")
html_message = """
🎯 <b>PRUEBA DE FORMATO</b>

🎮 <b>Juego de prueba</b>
💰 Precio: <s>59.99€</s>
💸 <b>AHORA: 29.99€</b>

🛒 <b>Link:</b>
👉 https://www.instant-gaming.com/es/?igr=gamer-a4609b2
"""

try:
    response = requests.post(
        url,
        data={
            "chat_id": CANAL_ID,
            "text": html_message.strip(),
            "parse_mode": "HTML"
        },
        timeout=15
    )
    
    print(f"   Status: {response.status_code}")
    print(f"   Respuesta: {response.text[:200]}")
    
    if response.status_code == 200 and response.json().get("ok"):
        print("✅ Mensaje HTML enviado correctamente")
    else:
        print(f"❌ Fallo HTML: {response.json().get('description', 'Error desconocido')}")
        
except Exception as e:
    print(f"❌ Error: {e}")

# 4. Probar mensaje simple (sin formato)
print(f"\n4️⃣ Probando mensaje simple...")
simple_message = "🎮 Oferta: Juego de prueba - 29.99€ - https://www.instant-gaming.com/es/?igr=gamer-a4609b2"

try:
    response = requests.post(
        url,
        data={
            "chat_id": CANAL_ID,
            "text": simple_message
        },
        timeout=15
    )
    
    print(f"   Status: {response.status_code}")
    print(f"   Respuesta: {response.text[:200]}")
    
    if response.status_code == 200 and response.json().get("ok"):
        print("✅ Mensaje simple enviado")
    else:
        print(f"❌ Fallo: {response.json().get('description', 'Error')}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ DIAGNÓSTICO COMPLETADO")
print("=" * 60)
print("\n📋 Revisa los mensajes en tu canal de Telegram")
print("Si no ves ningún mensaje, comparte los logs completos")
