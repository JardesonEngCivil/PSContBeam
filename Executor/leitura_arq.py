import json

def leitura_dados(arquivo = "viga.json"):

    print(f"lendo os dados de entrado do arquivo {arquivo.upper()}")

    with open(arquivo, "r") as file:
        base_dados = json.load(file)
        return base_dados 

