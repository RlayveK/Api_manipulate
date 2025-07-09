import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

import os
import pandas as pd

gateway_path = os.getenv("GATEWAY_PATH")

def criar_csv(nome, dados):
    try:
        if not gateway_path:
            raise ValueError("A variável de ambiente 'GATEWAY_PATH' não está definida.")

        # Garantir que o caminho termine com separador
        caminho = os.path.join(gateway_path, nome)

        # Criar o DataFrame e salvar como CSV
        df = pd.DataFrame(dados)
        df.to_csv(caminho, index=False)

        return f"Arquivo '{nome}' criado com sucesso em: {caminho}"
    
    except Exception as e:
        return f"Erro ao criar o arquivo CSV: {str(e)}"

