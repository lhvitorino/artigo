from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpBinary

# Definir os dados (exemplo simples)
DM = [100, 200]         # Demanda medida
# pesos = [5, 8, 7, 6]    # pesos dos itens
Te1 = 2                 # tarifa com icms
Te2 = 1                 # tarfia sem icms

# Definir o problema de otimização (maximização)
custo = LpProblem("Modelo1_Demanda", LpMinimize)

# Definir variáveis de decisão binárias (0 ou 1) para cada item
bu = [LpVariable(f'bu{i}', cat=LpBinary) for i in range(len(DM))]
bnu = [LpVariable(f'bnu{i}', cat=LpBinary) for i in range(len(DM))]

# Definir variável inteira para a demanda
# DC = [LpVariable(f'DC{i}', lowBound=0, upBound = None, cat='LpInteger') for i in range(len(DM))]
dc = LpVariable("dc", lowBound=0, cat='LpInteger')

# Definir a função objetivo (minimizar a demanda contratada)
custo += lpSum([DM[i] + (DM[i]-dc) * 2 * Te1 * bu[i] + (dc-DM[i]) * Te2 * bnu[i] for i in range(len(DM))]), "Função Objetivo"

# Adicionar a restrição de peso (soma dos pesos dos itens selecionados <= peso máximo)
custo += lpSum([DM[i] - dc + bu[i] for i in range(len(DM))]) >= 0, "Restrição de Ultrapassagem"
custo += lpSum([DM[i] - dc + bnu[i] for i in range(len(DM))]) <= 0, "Restrição de Ultrapassagem"
custo += lpSum([bu[i] + bnu[i] for i in range(len(DM))]) >= 1, "Restrição de Ultrapassagem"

# Resolver o problema
custo.solve()

# Exibir os resultados
print("Status:", custo.status)
print (dc.varValue)
for i in range(len(DM)):
    print(f'Item {i}: Selecionado = {bu[i].varValue}')
    print(f'Item {i}: Selecionado = {bnu[i].varValue}')

# Exibir o valor da função objetivo (valor total dos itens selecionados)
print(f'Valor total dos itens selecionados: {custo.objective.value()}')