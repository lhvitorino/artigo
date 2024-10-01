from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpBinary, LpInteger

# Definir os dados (exemplo simples)
dm = [100, 200, 120, 90]         # Demanda medida
Te1 = 2                 # tarifa com ICMS
Te2 = 1                 # tarifa sem ICMS

# Definir o problema de otimização (minimização)
custo = LpProblem("Modelo1_Demanda", LpMinimize)

# Definir variável inteira para a demanda
dc = LpVariable('dc', lowBound=0, upBound=None, cat=LpInteger)

# Definir variáveis de decisão binárias (0 ou 1) para cada item
bu = [LpVariable(f'bu{i}', cat=LpBinary) for i in range(len(dm))]
bnu = [LpVariable(f'bnu{i}', cat=LpBinary) for i in range(len(dm))]

# Linearização: você pode criar variáveis auxiliares que representem as subtrações envolvidas
z1 = [LpVariable(f'z1_{i}', lowBound=0, upBound=None) for i in range(len(dm))]  # Representa (DM[i] - DC[i]) * bu[i]
z2 = [LpVariable(f'z2_{i}', lowBound=0, upBound=None) for i in range(len(dm))]  # Representa (DC[i] - DM[i]) * bnu[i]

# Restrições de linearização para z1 e z2
for i in range(len(dm)):
    custo += z1[i] >= dm[i] - 1.05 * dc- (1 - bu[i]) * 1000  # Valor grande para forçar a linearização
    custo += z1[i] <= bu[i] * 1000
    custo += z2[i] >= dc - dm[i] - (1 - bnu[i]) * 1000
    custo += z2[i] <= bnu[i] * 1000

# Definir a função objetivo (minimizar a demanda contratada com base na linearização)
custo += lpSum([dm[i] + z1[i] + z2[i] for i in range(len(dm))]), "Função Objetivo"

# Adicionar restrições
custo += lpSum([dm[i] - dc + bu[i] for i in range(len(dm))]) >= 0, "Restrição de Ultrapassagem 1"
custo += lpSum([dm[i] - dc + bnu[i] for i in range(len(dm))]) <= 0, "Restrição de Ultrapassagem 2"
custo += lpSum([bu[i] + bnu[i] for i in range(len(dm))]) >= 1, "Restrição de Ultrapassagem 3"

# Resolver o problema
custo.solve()

# Exibir os resultados
print("Status:", custo.status)
print(dc.varValue)
for i in range(len(dm)):
    print(f'Item {i}: Selecionado = {bu[i].varValue}')
    print(f'Item {i}: Selecionado = {bnu[i].varValue}')

# Exibir o valor da função objetivo (valor total dos itens selecionados)
print(f'Valor total do custo: {custo.objective.value()}')
