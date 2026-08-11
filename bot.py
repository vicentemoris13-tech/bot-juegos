import os, requests, time
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = os.environ.get("CANAL_ID")
AFILIADO = "gamer-a4609b2"

print(f"=== INICIANDO ===")
print(f"CANAL_ID es: {CANAL_ID}")
print(f"TOKEN existe: {bool(TOKEN)}")

def enviar(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": CANAL_ID, "text": texto}, timeout=20)
        print(f"Respuesta: {r.text}")
        return r.json().get("ok", False)
    except Exception as e:
        print(f"ERROR en enviar: {e}")
        return False

# PRUEBA 1 SOLA PRIMERO
ok = enviar("✅ TEST 1 - Si ves esto, el bot funciona")
print(f"Resultado test: {ok}")

# Si el test funcionó, mandamos los 5
if ok:
    juegos = ["GTA V", "Red Dead 2", "Cyberpunk", "Elden Ring", "Witcher 3"]
    for j in juegos:
        link = f"https://www.instant-gaming.com/es/buscar/?q={j}&igr={AFILIADO}"
        enviar(f"🔥 {j}\n💸 {link}")
        time.sleep(5)

print("=== FIN ===")
