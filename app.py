
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from collections import Counter
import urllib.request
import alpaca_trade_api as tradeapi

app = Flask(__name__)
CORS(app) 

# --- RUTA 1: FÓRMULA MÁGICA ---
@app.route('/api/formula-magica', methods=['GET'])
def obtener_ganadoras():
    try:
        with open('datos_empresas.json', 'r') as archivo:
            empresas = json.load(archivo)
        empresas.sort(key=lambda x: x['roic'], reverse=True)
        for i, emp in enumerate(empresas): emp['rango_roic'] = i + 1
        empresas.sort(key=lambda x: x['earnings_yield'], reverse=True)
        for i, emp in enumerate(empresas): emp['rango_ey'] = i + 1
        for emp in empresas: emp['puntaje_magico'] = emp['rango_roic'] + emp['rango_ey']
        ganadoras = sorted(empresas, key=lambda x: x['puntaje_magico'])
        return jsonify(ganadoras[:3]) 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- RUTA 2: FONDOS GURÚS 13F ---
@app.route('/api/gurus', methods=['GET'])
def obtener_datos_gurus():
    portafolios_13f = {
        "1. Warren Buffett (Berkshire Hathaway)": ["AAPL", "BAC", "AXP", "CVX", "KO"],
        "2. Ray Dalio (Bridgewater Associates)": ["PG", "JNJ", "PEP", "MCD", "WMT"],
        "3. Bill Ackman (Pershing Square)": ["CMG", "QSR", "HLT", "GOOGL", "CP"],
        "4. Ken Fisher (Fisher Investments)": ["AAPL", "MSFT", "AMZN", "GOOGL", "NVDA"],
        "5. David Tepper (Appaloosa Management)": ["META", "GOOGL", "AMZN", "MSFT", "NVDA"],
        "6. Carl Icahn (Icahn Enterprises)": ["IEP", "CVI", "OXY", "SWX", "NWL"],
        "7. George Soros (Soros Fund Management)": ["QQQ", "AMZN", "GOOGL", "MSFT", "CRM"],
        "8. Howard Marks (Oaktree Capital)": ["VSTRA", "TRMD", "STNG", "VALE", "C"],
        "9. Seth Klarman (Baupost Group)": ["LBTYK", "QRVO", "VSAT", "WBD", "GOOGL"],
        "10. Stanley Druckenmiller (Duquesne)": ["NVDA", "MSFT", "LLY", "META", "AMZN"]
    }
    todas_las_acciones = []
    for acciones in portafolios_13f.values(): todas_las_acciones.extend(acciones)
    conteo = Counter(todas_las_acciones)
    consenso_top_4 = [{"ticker": ticker, "votos": votos} for ticker, votos in conteo.most_common(4)]
    return jsonify({"consenso": consenso_top_4, "gurus": portafolios_13f})

# --- RUTA 3: FONDO CRYPTO + SENTIMIENTO ---
@app.route('/api/crypto', methods=['GET'])
def obtener_datos_crypto():
    try:
        req = urllib.request.urlopen('https://api.alternative.me/fng/?limit=1')
        respuesta_api = json.loads(req.read())
        valor_fng = respuesta_api['data'][0]['value']
        clasificacion_fng = respuesta_api['data'][0]['value_classification']
    except Exception:
        valor_fng = "50"
        clasificacion_fng = "Neutral (Error de conexión)"

    senales = [
        {"ticker": "BTC/USD", "nombre": "Bitcoin", "senal": "COMPRA FUERTE", "peso": "50%"},
        {"ticker": "ETH/USD", "nombre": "Ethereum", "senal": "MANTENER", "peso": "30%"},
        {"ticker": "SOL/USD", "nombre": "Solana", "senal": "COMPRA", "peso": "20%"}
    ]
    
    return jsonify({
        "senales": senales,
        "sentimiento": {"valor": valor_fng, "clasificacion": clasificacion_fng}
    })

# --- RUTA 4: EJECUTAR ORDEN EN ALPACA (GURÚS) ---
@app.route('/api/invertir/gurus', methods=['POST'])
def invertir_en_gurus():
    datos = request.json
    capital = float(datos.get('capital')) 
    
    print(f"💰 Orden de ${capital} recibida. Conectando con Alpaca...")

    # ¡PON TUS LLAVES NUEVAS AQUÍ!
    API_KEY = "PKXKF4M632HTBHYCGGDDUKGK45"
    SECRET_KEY = "6fSTQUVj1nGFkwAm5661Ye712WMwPhHCVCC4Yx6W9bie"
    BASE_URL = "https://paper-api.alpaca.markets"
    
    try:
        api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
        acciones = ['GOOGL', 'MSFT', 'AMZN', 'NVDA']
        monto_por_accion = capital / len(acciones)
        
        for ticker in acciones:
            api.submit_order(
                symbol=ticker,
                notional=monto_por_accion,
                side='buy',
                type='market',
                time_in_force='day'
            )
            print(f"✅ Orden enviada: ${monto_por_accion} de {ticker}")
            
        return jsonify({"estatus": "exito", "mensaje": "Orden ejecutada. Revisa tu panel de Alpaca."})
        
    except Exception as e:
        print(f"❌ Error en Alpaca: {e}")
        return jsonify({"estatus": "error", "mensaje": str(e)}), 500

# --- RUTA 5: EJECUTAR ORDEN CRYPTO EN ALPACA ---
@app.route('/api/invertir/crypto', methods=['POST'])
def invertir_en_crypto():
    datos = request.json
    capital = float(datos.get('capital')) 
    
    print(f"⚡ Orden Crypto de ${capital} recibida. Ejecutando 24/7...")

    # ¡PON TUS MISMAS LLAVES NUEVAS AQUÍ TAMBIÉN!
    API_KEY = "PKXKF4M632HTBHYCGGDDUKGK45"
    SECRET_KEY = "6fSTQUVj1nGFkwAm5661Ye712WMwPhHCVCC4Yx6W9bie"
    BASE_URL = "https://paper-api.alpaca.markets"
    
    try:
        api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
        ticker = 'BTC/USD'
        
        api.submit_order(
            symbol=ticker,
            notional=capital,
            side='buy',
            type='market',
            time_in_force='gtc' 
        )
        print(f"✅ Orden Crypto enviada: ${capital} de {ticker}")
            
        return jsonify({"estatus": "exito", "mensaje": f"Compraste ${capital} USD en Bitcoin exitosamente."})
        
    except Exception as e:
        print(f"❌ Error en Alpaca Crypto: {e}")
        return jsonify({"estatus": "error", "mensaje": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Servidor Flask iniciado. Escuchando múltiples rutas...")
    app.run(debug=True, port=5000)