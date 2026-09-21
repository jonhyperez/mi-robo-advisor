import time
import urllib.request
import json
import alpaca_trade_api as tradeapi
from datetime import datetime

# --- 1. TUS CREDENCIALES DE ALPACA (PAPER TRADING) ---
API_KEY = "PKXKF4M632HTBHYCGGDDUKGK45"
SECRET_KEY = "6fSTQUVj1nGFkwAm5661Ye712WMwPhHCVCC4Yx6W9bie"
BASE_URL = "https://paper-api.alpaca.markets"

# Conexión con el broker
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

def analizar_y_comprar():
    hora_actual = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{hora_actual}] 🤖 [PILOTO AUTOMÁTICO] Analizando mercado Cripto...")
    
    try:
        # FASE A: ANÁLISIS (Consulta el índice Fear & Greed en vivo)
        req = urllib.request.urlopen('https://api.alternative.me/fng/?limit=1')
        respuesta = json.loads(req.read())
        valor_mercado = int(respuesta['data'][0]['value'])
        estado = respuesta['data'][0]['value_classification']
        
        print(f"📊 Estado del mercado: {valor_mercado}/100 ({estado})")
        
        # FASE B: REGLA MATEMÁTICA Y DECISIÓN
        # Para esta prueba comprará si el valor es menor a 100 (comprará de inmediato).
        # En producción real, cambiarás este 100 por 45 (para comprar solo cuando hay Miedo/Oportunidad).
        if valor_mercado < 100:
            capital = 1000.0  # $1,000 USD de tu saldo virtual
            ticker = 'BTC/USD'
            
            print(f"🎯 Oportunidad detectada. Comprando ${capital} USD en {ticker}...")
            
            # FASE C: EJECUCIÓN AUTOMÁTICA EN ALPACA
            api.submit_order(
                symbol=ticker,
                notional=capital,
                side='buy',
                type='market',
                time_in_force='gtc' # Good Till Cancelled
            )
            print("✅ ¡COMPRA REALIZADA! Se agregó Bitcoin a tu portafolio en Alpaca.")
        else:
            print("⏳ El mercado está muy costoso. El bot esperará al siguiente ciclo.")
            
    except Exception as e:
        print(f"❌ Error en el ciclo del bot: {e}")

# --- BUCLE CONTINUO (SEGUNDO PLANO) ---
if __name__ == '__main__':
    print("🚀 JF Investments: Bot Autónomo Iniciado.")
    print("Evaluando el mercado automáticamente cada 60 segundos...\n")
    
    while True:
        analizar_y_comprar()
        print("💤 Bot en reposo. Próximo análisis en 60 segundos...")
        time.sleep(60) # Espera 1 minuto antes de volver a analizar