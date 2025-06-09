import json
import requests
from dotenv import load_dotenv
import os


load_dotenv()

app_token = os.getenv("app_token")
access_token = os.getenv("access_token")

URL_PLANO_CONTAS = 'https://api.superlogica.net/v2/financeiro/planocontas/index/id/0?itensPorPagina=150&pagina='

HEADERS = {
    'Content-type': 'application/x-www-form-urlencoded',
    'app_token': app_token,
    'access_token': access_token
}

def getPlano():

    linhas = []
    status = []
    i = 1

    try:
        while True:
            response = requests.get(URL_PLANO_CONTAS + str(i), headers=HEADERS)
            dados = json.loads(response.content)
            if isinstance(dados, list) and len(dados) > 0:
                status.append(response.status_code)
                
                for item in dados:
                    keys = {
                        "st_conta_cont", "st_descricao_cont", "st_ordenacao_cont"
                    }
                    linha = {k: v for k, v in item.items() if k in keys}
                    linhas.append(linha)                
                i += 1
            else:
                break
    except Exception as e:
        print("Erro na página: ", i)
        print(response.status_code)
    return linhas

