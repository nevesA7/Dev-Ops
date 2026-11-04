import requests

# Código das séries temporais no SGS do Banco Central
BCB_SERIES = {
    "dolar": 1,     # Cotação do Dólar (Venda)
    "selic": 11,    # Taxa Selic (% ao mês)
    "ipca": 433     # IPCA (% ao mês)
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

def get_all_bcb_data():
    return {
        "dolar": fetch_bcb_series(BCB_SERIES["dolar"]),
        "selic": fetch_bcb_series(BCB_SERIES["selic"]),
        "ipca": fetch_bcb_series(BCB_SERIES["ipca"])
    }