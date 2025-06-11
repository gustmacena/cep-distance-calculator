import requests
import math
import pandas as pd
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_coordinates_from_cep(cep, retries=3, delay=1):
    cep = ''.join(filter(str.isdigit, str(cep)))
    if len(cep) != 8:
        return None, None

    # 1. Tenta BrasilAPI
    url_brasilapi = f"https://brasilapi.com.br/api/cep/v2/{cep}"
    for i in range(retries):
        try:
            response = requests.get(url_brasilapi, timeout=10)
            if response.status_code == 200:
                data = response.json()
                location = data.get("location", {})
                coords = location.get("coordinates", {})
                lat = coords.get("latitude")
                lon = coords.get("longitude")
                if lat and lon:
                    return float(lat), float(lon)
            break  # sai do loop se não encontrar
        except:
            time.sleep(delay)

    # 2. Fallback para Nominatim (OpenStreetMap)
    try:
        url_nominatim = f"https://nominatim.openstreetmap.org/search?format=json&postalcode={cep}&country=Brazil"
        response = requests.get(url_nominatim, headers={"User-Agent": "cep-distance-calc"}, timeout=10)
        if response.status_code == 200:
            results = response.json()
            if results:
                lat = results[0]['lat']
                lon = results[0]['lon']
                return float(lat), float(lon)
    except:
        pass

    return None, None

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

if __name__ == "__main__":
    arquivo_excel = r"C:\Users\gustavocm\Desktop\TesteE-commerce\Distancia de CEP\DistanciadeCEP.xlsx"
    df = pd.read_excel(arquivo_excel)

    # Garante que a coluna E esteja pronta para receber valores mistos
    if df.shape[1] >= 5:
        col_e = df.columns[4]
        df[col_e] = df[col_e].astype("object")
    else:
        df.insert(4, "Distancia", None)
        col_e = "Distancia"

    # Lista de pares de CEPs
    lista_cep = [(index, str(row["CEP Centro"]), str(row["CEP Destino"])) for index, row in df.iterrows()]
    resultados = {}

    print("🔄 Consultando CEPs em paralelo (BrasilAPI + fallback Nominatim)...")
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_index = {
            executor.submit(get_coordinates_from_cep, centro): (index, 'centro', centro)
            for index, centro, _ in lista_cep
        }
        future_to_index.update({
            executor.submit(get_coordinates_from_cep, destino): (index, 'destino', destino)
            for index, _, destino in lista_cep
        })

        for future in tqdm(as_completed(future_to_index), total=len(future_to_index)):
            index, tipo, cep = future_to_index[future]
            lat, lon = future.result()
            if index not in resultados:
                resultados[index] = {}
            resultados[index][f"{tipo}_lat"] = lat
            resultados[index][f"{tipo}_lon"] = lon

    # Calcula distância
    for index in tqdm(range(len(df)), desc="🧮 Calculando distâncias"):
        dados = resultados.get(index, {})
        if all(k in dados and dados[k] is not None for k in ["centro_lat", "centro_lon", "destino_lat", "destino_lon"]):
            dist = haversine_distance(
                dados["centro_lat"], dados["centro_lon"],
                dados["destino_lat"], dados["destino_lon"]
            )
            df.iat[index, 4] = round(dist, 2)
        else:
            df.iat[index, 4] = "Erro ao calcular"

    df.to_excel(arquivo_excel, index=False)
    print(f"\n✅ Distâncias calculadas e salvas com fallback no arquivo:\n{arquivo_excel}")
