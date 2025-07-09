import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app_token = os.getenv("app_token")
access_token = os.getenv("access_token")

URL_BASE = 'https://api.superlogica.net/v2/financeiro/clientes?itensPorPagina=200&status={status}&pagina={pagina}'

HEADERS = {
    'Content-type': 'application/x-www-form-urlencoded',
    'app_token': app_token,
    'access_token': access_token
}

def getClientesPorStatus(status_valor):
    clientes_status = []
    i = 1

    try:
        while True:
            url = URL_BASE.format(status=status_valor, pagina=i)
            response = requests.get(url, headers=HEADERS)
            dados = json.loads(response.content)

            if isinstance(dados, list) and len(dados) > 0:
                for item in dados:
                    keys = {
                        "st_sincro_sac", "id_sacado_sac", "st_nome_sac", 
                        "st_cgc_sac", "dt_cadastro_sac", "dt_desativacao_sac"
                    }
                    linha = {k: v for k, v in item.items() if k in keys}
                    linha["Status"] = "ativo" if status_valor == 0 else "inativo"
                    clientes_status.append(linha)
                i += 1
            else:
                break
    except Exception as e:
        print(f"Erro na página {i} (status={status_valor}):", str(e))
        print("Status code:", response.status_code if response else "N/A")

    return clientes_status

def getTodosClientes():
    clientes_ativos = getClientesPorStatus(0)
    clientes_inativos = getClientesPorStatus(1)
    return clientes_ativos + clientes_inativos
