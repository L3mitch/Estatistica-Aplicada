
from detector import *
import time
import requests
# python -m pip install requests


# requisicoes = [{"id": 1, "tipo": 0, "nome": "nome_aqui", "processado": 0, "sucesso": 0},]
requisicoes = [[69, 2, "kauan_nunes", 0, 0],
               [70, 86, "michel_jackson", 0, 0]
               ]
# Formato da lista de requisicoes:
# [ID, tipo, nome, processado, sucesso]
# 0 - ID da requisicao: referência para responder a requisição
# 1 - Tipo da requisicao: 0 - Adicionar face, Qualquer outro valor - Reconhecer face (ID da imagem a reconhecer)
# 2 - Nome da pessoa
# 3 - Processado: 0 - Não processado, 1 - Processado (Esse valor não é passado na requisição)
# 4 - Sucesso: 0 - Falha, 1 - Sucesso ()

def ler_requisicoes():
    url = "http://localhost:3000/requisicoes"
    response = requests.get(url)
    return response.json()

def enviar_resposta(requisicao):
    url = "http://localhost:3000/requisicoes"
    data = {requisicao}
    response = requests.post(url, data=data)
    return response.json()


while True:
    # Tratamento da requisição
    for requisicao in requisicoes:
        if requisicao[3] == 1:
            break
        if requisicao[1] == 0: # Adicionar face
            requisicao[4] = encode_new_face(requisicao[2], model="hog")
        else:
            requisicao[4] = match_face(requisicao[2], requisicao[1], model="hog")
        requisicao[3] = 1

    if(requisicoes): print(requisicoes)

    # Resposta da requisição
    for requisicao in requisicoes:
        if requisicao[3] == 1:
            # enviar_resposta(requisicao)
            print(requisicao)
            requisicoes.remove(requisicao)
    time.sleep(1)