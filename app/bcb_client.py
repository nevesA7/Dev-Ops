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
    
    # Tentativa 1: AwesomeAPI (rota /json/last/)
    try:
        url_awesome = "https://economia.awesomeapi.com.br/json/last/BTC-BRL"
        response = requests.get(url_awesome, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json().get("BTCBRL", {})
            bid = float(data.get("bid", 0))
            if bid > 0:
                return {
                    "valor": bid,
                    "variacao": data.get("pctChange", "0")
                }
    except Exception as e:
        print(f"AwesomeAPI Bitcoin error: {e}")

    # Tentativa 2 (Fallback): Mercado Bitcoin
    try:
        url_mb = "https://www.mercadobitcoin.net/api/BTC/ticker/"
        response = requests.get(url_mb, headers=headers, timeout=5)
        if response.status_code == 200:
            ticker = response.json().get("ticker", {})
            last_val = float(ticker.get("last", 0))
            if last_val > 0:
                return {
                    "valor": last_val,
                    "variacao": "0"
                }
    except Exception as e:
        print(f"Mercado Bitcoin error: {e}")

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