import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpInteger

# Carregar os dados do arquivo CSV
# Exemplo: suponha que o arquivo contenha colunas 'custo', 'recurso1', 'recurso2'
df = pd.read_csv('seu_arquivo.csv')

# Definir o problema de programação linear mista (maximização ou minimização)
problema = LpProblem("Exemplo_de_Problema_MILP", LpMaximize)

# Definir as variáveis de decisão (binárias ou inteiras)
# Exemplo: criar uma variável binária x para cada item no dataframe
x = [LpVariable(f'x{i}', cat=LpInteger, lowBound=0, upBound=1) for i in range(len(df))]

# Definir a função objetivo (exemplo de maximização do lucro)
problema += lpSum(df['custo'][i] * x[i] for i in range(len(df))), "Função Objetivo"

# Adicionar restrições (exemplo: limite de recurso1 <= 100 e recurso2 <= 50)
problema += lpSum(df['recurso1'][i] * x[i] for i in range(len(df))) <= 100, "Restrição Recurso1"
problema += lpSum(df['recurso2'][i] * x[i] for i in range(len(df))) <= 50, "Restrição Recurso2"

# Resolver o problema
problema.solve()

# Exibir os resultados
print("Status:", problema.status)
for i in range(len(df)):
    print(f'Item {i}: {x[i].varValue}')

# Exibir o valor da função objetivo
print(f'Valor ótimo da função objetivo: {problema.objective.value()}')
