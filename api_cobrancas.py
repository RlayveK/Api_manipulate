import json
import requests
from dotenv import load_dotenv
import os


load_dotenv()

app_token = os.getenv("app_token")
access_token = os.getenv("access_token")

URL_PLANO_CONTAS = 'https://api.superlogica.net/v2/financeiro/cobranca?dtInicio=01/01/2024&exibirComposicaoDosBoletos=1&itensPorPagina=100&status=todos&dtFim=12/31/2025&pagina='

HEADERS = {
    'Content-type': 'application/x-www-form-urlencoded',
    'app_token': app_token,
    'access_token': access_token
}

def getCobs():

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
                        "id_sacado_sac", "st_sincro_sac", "st_cgc_sac", "compo_recebimento", "id_recebimento_recb","fl_status_recb", 
                        "dt_vencimento_recb", "dt_recebimento_recb","dt_liquidacao_recb", "dt_cancelamento_recb", "id_nota_not", 
                        "id_formapagamento_recb", "dt_competencia_recb", "fl_motivocancelar_recb"
                    }
                    linha = {k: v for k, v in item.items() if k in keys}
                    composicao = []
                    for chave in ["compo_recebimento"]:
                        if chave in linha:                        
                            composicao += [                                              
                                {
                                    "st_descricao_prd": a.get("st_descricao_prd"),
                                    "st_mesano_comp": a.get("st_mesano_comp"),
                                    "st_descricao_comp": a.get("st_descricao_comp"),
                                    "st_valor_comp": a.get("st_valor_comp"),
                                    "nm_quantidade_comp": a.get("nm_quantidade_comp"),
                                    "id_produto_prd": a.get("id_produto_prd"),
                                    "st_complemento_comp": a.get("st_complemento_comp")
                                }
                                for a in linha[chave] if "st_descricao_prd" in a
                            ]   
                    linha["compo_recebimento"] = composicao
                    linhas.append(linha)    
                i += 1
                if i%25 == 0:
                    print("Páginas: "+str(i))
            else:
                break
    except Exception as e:
        print("Erro na página: ", i)
        print(response.status_code)
    return linhas

