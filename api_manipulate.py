import json
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import ctypes

load_dotenv()

app_token = os.getenv("app_token")
access_token = os.getenv("access_token")

URL_DESPESAS = 'https://api.superlogica.net/v2/financeiro/despesas?dtInicio=01/01/2025&flstatus=1&pagina='
URL_CAIXA = 'https://api.superlogica.net/v2/financeiro/caixa?flcreditodebito=2&flstatus=0&id='
HEADERS = {
    'Content-type': 'application/x-www-form-urlencoded',
    'app_token': app_token,
    'access_token': access_token
}


def barra_progresso(atual, total, comprimento=30):
    proporcao = atual / total
    preenchido = int(comprimento * proporcao)
    barra = '*' * preenchido + '-' * (comprimento - preenchido)
    print(f'\r|{barra}| {proporcao * 100:.2f}%', end='', flush=True)


def getDespesas():
    print(f"\n\n--- Execução em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ---")

    ids = []
    linhas = []
    status = []
    i = 1

    try:
        while True:
            response = requests.get(URL_DESPESAS + str(i), headers=HEADERS)
            dados = json.loads(response.content)
            if isinstance(dados, list) and len(dados) > 0:
                ids.extend(item['id_contabanco_mov'] for item in dados)
                status.append(response.status_code)
                i += 1
            else:
                break
    except Exception as e:
        print("Erro na página: ", i)
        print(response.status_code)

    print(f"Sucessos na primeira requisição: {len(status)}")
    print(f"Quantidade de Ids: {len(ids)}")

    for idx, id_mov in enumerate(ids):
        response_aprop = requests.get(URL_CAIXA + id_mov, headers=HEADERS)
        aprop = json.loads(response_aprop.content)
        barra_progresso(idx + 1, len(ids))

        for item in aprop:
            keys = {
                "id_contabanco_mov", "dt_lancamento_mov", "dt_vencimento_mov",
                "dt_liquidacao_mov", "st_historico_mov", "vl_valor_mov", "apropriacao",
                "apropriacao_desconto", "centro_de_custo"
            }
            linha = {k: v for k, v in item.items() if k in keys}

            apropriacoes = []
            for chave in ["apropriacao", "apropriacao_desconto"]:
                if chave in linha:
                    apropriacoes += [
                        {
                            "st_conta_cont": a.get("st_conta_cont"),
                            "st_complemento_mov": a.get("st_complemento_mov"),
                            "st_descricao_cont": a.get("st_descricao_cont"),
                            "vl_apropriacao": a.get("vl_apropriacao"),
                            "nm_participacao_mova": a.get("nm_participacao_mova")
                        }
                        for a in linha[chave] if "st_conta_cont" in a
                    ]

            linha["apropriacao"] = apropriacoes
            linha.pop("apropriacao_desconto", None)

            if "centro_de_custo" in linha:
                linha["centro_de_custo"] = [
                    {
                        "st_descricao_cc": cc.get("st_descricao_cc"),
                        "vlparticipacao": cc.get("vlparticipacao")
                    }
                    for cc in linha["centro_de_custo"] if "st_descricao_cc" in cc
                ]

            linhas.append(linha)
           
    # ctypes.windll.user32.MessageBoxW(0, "Script executado com sucesso!", "Notificação", 0x40)
    return linhas
