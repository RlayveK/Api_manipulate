import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

gateway_path = os.getenv("GATEWAY_PATH")


def save_json(dados, nome_arquivo):
    caminho = os.path.join(gateway_path, nome_arquivo)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)  # cria diretórios se não existirem
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump({"dados": dados}, f, ensure_ascii=False, indent=2)

def criar_json(dados, nome_arquivo):
    try:   
        save_json(dados, nome_arquivo)
        print("\n[INFO] JSON atualizado com sucesso.")
    except Exception as e:
        print(f"[ERRO] Falha ao atualizar JSON: {e}")

def append_to_json(novos_dados, nome_arquivo, chave_unica=None, controle_nome="controle_execucao.json"):
    caminho = os.path.join(gateway_path, nome_arquivo)
    controle_path = os.path.join(gateway_path, controle_nome)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    dados_existentes = []

    # Lê dados existentes (se houver)
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = json.load(f)
                if "dados" in conteudo and isinstance(conteudo["dados"], list):
                    dados_existentes = conteudo["dados"]
        except Exception as e:
            print(f"[AVISO] Erro ao carregar JSON existente: {e}")

    # Evita duplicação com base em chave única
    if chave_unica:
        ids_existentes = {item[chave_unica] for item in dados_existentes if chave_unica in item}
        novos_dados = [item for item in novos_dados if item.get(chave_unica) not in ids_existentes]

    # Atualiza e salva
    dados_atualizados = dados_existentes + novos_dados

    try:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump({"dados": dados_atualizados}, f, ensure_ascii=False, indent=2)

        # Atualiza o arquivo de controle com a data de hoje
        hoje = datetime.today().strftime("%Y-%m-%d")
        with open(controle_path, "w", encoding="utf-8") as fc:
            json.dump({"ultima_execucao": hoje}, fc, ensure_ascii=False, indent=2)

        print(f"[INFO] {len(novos_dados)} novos registros adicionados com sucesso.")
        print(f"[INFO] Controle de execução atualizado para {hoje}.")

    except Exception as e:
        print(f"[ERRO] Falha ao salvar JSON atualizado: {e}")

def deve_executar(controle_nome="controle_execucao.json"):
    controle_path = os.path.join(gateway_path, controle_nome)
    hoje = datetime.today().date()
    dia = hoje.day

    # Fora do intervalo permitido (1 a 5)
    if dia > 5:
        print(f"[INFO] Fora do período permitido (1 a 5). Hoje é dia {dia}.")
        return False

    # Se controle não existe, nunca executou — pode rodar
    if not os.path.exists(controle_path):
        return True

    try:
        with open(controle_path, "r", encoding="utf-8") as f:
            controle = json.load(f)
            ultima = controle.get("ultima_execucao")
            if ultima:
                data_ultima = datetime.strptime(ultima, "%Y-%m-%d").date()
                # Já executou neste mês?
                if data_ultima.year == hoje.year and data_ultima.month == hoje.month:
                    print(f"[INFO] Já executado em {ultima}. Aguarde o próximo mês.")
                    return False
    except Exception as e:
        print(f"[AVISO] Erro ao verificar controle de execução: {e}")
        return True  # Executa por precaução se leitura falhar

    return True  # Dentro do intervalo e ainda não executado este mês
