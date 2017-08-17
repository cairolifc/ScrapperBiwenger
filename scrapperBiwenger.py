import urllib.request
import json
from pprint import pprint

URL_BASE = 'https://biwenger.as.com/api/v1/home'
URL_NEWS = 'https://biwenger.as.com/api/v1/league/news?limit=10000&offset=0'
HEADERS = {

	#Sustituye los puntos suspensivos por etu codigo de autorización
    'Authorization': 'Bearer ... ',
    #liga 1 - Pon entre comillas tu codigo x-league 
    'x-league': ''
    #liga 2 'x-league': ''


}

news_url = URL_NEWS
base_url = URL_BASE

reqNews = urllib.request.Request(
    news_url,
    data=None,
    headers= HEADERS
)

reqBase = urllib.request.Request(
    base_url,
    data=None,
    headers= HEADERS
)

fBase = urllib.request.urlopen(reqBase)
responseBase = fBase.read().decode('utf-8')

fNews = urllib.request.urlopen(reqNews)
responseNews = fNews.read().decode('utf-8')

dataBase = json.loads(responseBase)
dataNews = json.loads(responseNews)

options = dataBase["data"]
league = options["league"]
standings = league["standings"]

carteraGasto = {}
lista = []

for teamName in standings:
    carteraGasto[teamName["name"]] = 0
    lista.append((carteraGasto))

#print("---- Inicializamos cartera ----")
#print(carteraGasto)


for item in dataNews["data"]:

    # Ganancias por venta de jugadores

    if item["type"] == "transfer":
        for vendidos in item["content"]:
            ingreso = vendidos["amount"]
            equipo = vendidos["from"]["name"]

            if 'to' not in vendidos:
                carteraGasto[equipo] += ingreso

            else:
                equipoDestino = vendidos["to"]["name"]
                carteraGasto[equipo] += ingreso
                carteraGasto[equipoDestino] -= ingreso

# Gastos por compra de jugadores

    if item["type"] == "market":
        for comprados in item["content"]:

            gasto = comprados["amount"]
            equipo = comprados["to"]["name"]
            carteraGasto[equipo] -= gasto

print("-----GASTOS POST COMPRAVENTAS----")
pprint(carteraGasto)



