import pulp

# Definir o modelo de otimização (minimização)
model = pulp.LpProblem("Minimize Energy Demand", pulp.LpMinimize)

# Definir os parâmetros (Dmi para cada mês i)
Dmi = [300, 320, 310, 305, 315, 300, 330, 340, 320, 310, 300, 315]  # Exemplo de demanda para 12 meses

# Variáveis de decisão
DC = pulp.LpVariable('DC', lowBound=0, cat='Integer')  # DC deve ser inteiro
a = pulp.LpVariable.dicts('a', range(12), cat='Binary')  # Variáveis binárias a_i para cada mês
b = pulp.LpVariable.dicts('b', range(12), cat='Binary')  # Variáveis binárias b_i para cada mês

# Função objetivo
model += pulp.lpSum([(Dmi[i] - DC) * b[i] + (DC - Dmi[i]) * a[i] for i in range(12)])

# Valor grande M (suficientemente grande)
M = 1000

# Restrições para as variáveis binárias b_i e a_i usando a técnica grande-M
for i in range(12):
    model += b[i] * (1.05 * DC - Dmi[i]) <= M * (1 - b[i])  # b[i] = 1 se Dmi[i] > 1.05 * DCcls
    model += a[i] * (DC - Dmi[i]) <= M * (1 - a[i])  # a[i] = 1 se Dmi[i] < DC

# Resolver o modelo
model.solve()

# Exibir resultados
print("Status:", pulp.LpStatus[model.status])
print(f"Valor de DC: {DC.varValue}")
for i in range(12):
    print(f"a_{i}: {a[i].varValue}, b_{i}: {b[i].varValue}")
