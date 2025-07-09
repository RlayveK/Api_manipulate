import json
import requests
from dotenv import load_dotenv
import os


load_dotenv()

app_token = os.getenv("app_token")
access_token = os.getenv("access_token")

URL_p1 = 'https://api.superlogica.net/v2/financeiro/clientes?itensPorPagina=200&status=2&pagina='

HEADERS = {
    'Content-type': 'application/x-www-form-urlencoded',
    'app_token': app_token,
    'access_token': access_token
}

def getClientes():

    linhas = []
    status = []
    i = 1

    try:
        while True:
            response = requests.get(URL_p1  + str(i), headers=HEADERS)
            dados = json.loads(response.content)
            if isinstance(dados, list) and len(dados) > 0:
                status.append(response.status_code)
                
                for item in dados:
                    keys = {
                        "st_sincro_sac", "id_sacado_sac","st_nome_sac", "st_cgc_sac","dt_cadastro_sac", "dt_desativacao_sac"
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

