import requests
from math import radians, sin, cos, sqrt, atan2
import logging

log = logging.getLogger(__name__)

def obter_endereco_via_cep(cep):
    try:
        log.info(f"Obtendo endereço para CEP: {cep}")
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        response.raise_for_status()
        data = response.json()
        if 'erro' in data:
            raise ValueError(f"CEP não encontrado: {cep}")
        return data
    except requests.RequestException as e:
        log.error(f"Erro ao obter endereço do CEP: {cep}. Erro: {e}")
        raise ValueError(f"Erro ao obter endereço do CEP: {cep}. Erro: {e}")

def obter_coordenadas(endereco):
    try:
        log.info(f"Obtendo coordenadas para o endereço: {endereco}")
        response = requests.get(f'https://geocode.maps.co/search', params={
            'q': f"{endereco['logradouro']}, {endereco['bairro']}, {endereco['localidade']}, {endereco['uf']}, Brazil",
        })
        response.raise_for_status()
        data = response.json()
        if not data:
            raise ValueError(f"Não foi possível obter as coordenadas para o endereço: {endereco}")
        return (float(data[0]['lat']), float(data[0]['lon']))
    except requests.RequestException as e:
        log.error(f"Erro ao obter coordenadas: {e}")
        raise ValueError(f"Erro ao obter coordenadas: {e}")

def calcular_distancia(origem_coords, destino_coords):
    log.info(f"Calculando distância entre {origem_coords} e {destino_coords}")
    R = 6371.0  # Raio da Terra em km

    lat1, lon1 = radians(origem_coords[0]), radians(origem_coords[1])
    lat2, lon2 = radians(destino_coords[0]), radians(destino_coords[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distancia = R * c
    log.info(f"Distância calculada: {distancia} km")
    return distancia
