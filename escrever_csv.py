import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

gateway_path = os.getenv("GATEWAY_PATH")

def criar_csv(nome, dados):
    try:
        caminho = gateway_path
        df = pd.DataFrame(dados)
        df.to_csv(caminho+nome, index=False)
        return(f"Arquivo {nome} criado com sucesso!")
    except Exception as e:
        print("Erro: ", e)
        
