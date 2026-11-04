import requests

BCB_SERIES = {
    "dolar": 1,     # Cotação Dólar
    "euro": 21619,   # Cotação Euro (Novo Data Source 1)
    "selic": 11,    # Taxa Selic
    "ipca": 433     # IPCA
}

def fetch_bcb_series(code, last_n=10):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados/ultimos/{last_n}?formato=json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Erro ao consultar série {code} do BCB: {e}")
    return []

def fetch_bitcoin():
    """Novo Data Source 2: AwesomeAPI (Bitcoin em R$)"""
    url = "https://economia.awesomeapi.com.br/last/BTC-BRL"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json().get("BTCBRL", {})
            return {
                "valor": float(data.get("bid", 0)),
                "variacao": data.get("pctChange", "0")
            }
    except Exception as e:
        print(f"Erro ao consultar Bitcoin: {e}")
    return {"valor": 0, "variacao": "0"}

def fetch_weather():
    """Novo Data Source 3: Open-Meteo (Temperatura Salvador/BA)"""
    url = "https://api.open-meteo.com/v1/forecast?latitude=-12.9711&longitude=-38.5108&current=temperature_2m,relative_humidity_2m"
    try:
        response = requests.get(url, timeout=5)
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