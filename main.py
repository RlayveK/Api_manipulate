from escrever_json import criar_json, append_to_json, deve_executar
from api_manipulate import getDespesas
from api_plano_de_contas import getPlano
from api_cobrancas import getCobs
from api_get_Grupo import getGrupo
from escrever_csv import criar_csv
from api_get_Clientes import getClientes
from api_cobrancas_inicioMes import getCobsInicio
import time 

criar_json(getPlano(), "plano_contas.json")
print("Plano de Contas criado com sucesso!")
print("esperando para próximas requisições: ")
time.sleep(30)

criar_json(getGrupo("104"), "WhiteLabels.json") 
print("WhiteLabels.json criado com sucesso!")
print("esperando para próximas requisições: ")
time.sleep(30)

criar_json(getGrupo("134"), "CredAtivosPrePagos.json")
print("CredAtivosPrePagos.json criado com sucesso!")
print("esperando para próximas requisições: ")
time.sleep(30)

criar_json(getGrupo("137"), "CredAtivosPosPagos.json")
print("CredAtivosPosPagos.json criado com sucesso!")
print("esperando para próximas requisições: ")
time.sleep(30)

criar_json(getGrupo("76"), "CredPosPagos.json")
print("CredPosPagos.json criado com sucesso!")
print("esperando para próximas requisições: ")
time.sleep(30)

criar_csv('Clientes.csv', getClientes())
print("Clientes.csv atualizado com sucesso")
print("esperando para próximas requisições: ")
time.sleep(30)

criar_json(getCobs(), "cobrancas.json")
if deve_executar():
    dados = getCobsInicio()
    append_to_json(dados, "cobsInicioMes.json", chave_unica="id_recebimento_recb")
    print("CobsInicioMes atualizado com sucesso!")
print("cobrancas atualizado com sucesso!")
print("esperando para próximas requisições: ")
time.sleep(30)

criar_json(getDespesas(), "despesas.json")

print("Concluído")