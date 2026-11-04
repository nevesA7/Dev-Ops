import requests

BCB_SERIES = {
    "dolar": 1,     # Cotação Dólar
    "euro": 21619,   # Cotação Euro
    "selic": 11,    # Taxa Selic
    "ipca": 433     # IPCA
}

def fetch_bcb_series(code, last_n=10):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados/ultimos/{last_n}?formato=json"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Erro ao consultar série {code} do BCB: {e}")
    return []

def fetch_bitcoin():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    # 1. Binance API (Principal: Resposta instantânea e sem bloqueio)
    try:
        url_binance = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCBRL"
        resp = requests.get(url_binance, headers=headers, timeout=4)
        if resp.status_code == 200:
            data = resp.json()
            val = float(data.get("lastPrice", 0))
            var = float(data.get("priceChangePercent", 0))
            if val > 0:
                return {"valor": val, "variacao": f"{var:.2f}"}
    except Exception as e:
        print(f"Binance BTC error: {e}")

    # 2. CoinGecko API (Fallback 1)
    try:
        url_coingecko = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl&include_24hr_change=true"
        resp = requests.get(url_coingecko, headers=headers, timeout=4)
        if resp.status_code == 200:
            data = resp.json().get("bitcoin", {})
            val = float(data.get("brl", 0))
            var = float(data.get("brl_24h_change", 0))
            if val > 0:
                return {"valor": val, "variacao": f"{var:.2f}"}
    except Exception as e:
        print(f"CoinGecko BTC error: {e}")

    # 3. AwesomeAPI (Fallback 2)
    try:
        url_awesome = "https://economia.awesomeapi.com.br/json/last/BTC-BRL"
        resp = requests.get(url_awesome, headers=headers, timeout=4)
        if resp.status_code == 200:
            data = resp.json().get("BTCBRL", {})
            val = float(data.get("bid", 0))
            var = float(data.get("pctChange", 0))
            if val > 0:
                return {"valor": val, "variacao": f"{var:.2f}"}
    except Exception as e:
        print(f"AwesomeAPI BTC error: {e}")

    return {"valor": 0, "variacao": "0"}

def fetch_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=-12.9711&longitude=-38.5108&current=temperature_2m,relative_humidity_2m"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            current = response.json().get("current", {})
            return {
                "temp": current.get("temperature_2m", "--"),
                "umidade": current.get("relative_humidity_2m", "--")
            }
    except Exception as e:
        print(f"Erro ao consultar Clima: {e}")
    return {"temp": "--", "umidade": "--"}

def get_all_bcb_data():
    return {
        "dolar": fetch_bcb_series(BCB_SERIES["dolar"]),
        "euro": fetch_bcb_series(BCB_SERIES["euro"]),
        "selic": fetch_bcb_series(BCB_SERIES["selic"]),
        "ipca": fetch_bcb_series(BCB_SERIES["ipca"]),
        "bitcoin": fetch_bitcoin(),
        "clima": fetch_weather()
    } 