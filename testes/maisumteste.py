import pulp

# Parâmetros de exemplo (demanda mensal)
Dmi = [300, 320, 310, 305, 315, 300, 330, 340, 320, 310, 300, 315]  # Demandas mensais
n = len(Dmi)
M = 100000  # Big-M (suficientemente grande)

# Criação do modelo
model = pulp.LpProblem("Minimize_costs", pulp.LpMinimize)

# Variável de decisão para DC (variável inteira)
DC = pulp.LpVariable('DC', lowBound=0, cat='Integer')

# Variáveis binárias b_i e a_i
b = [pulp.LpVariable(f'b_{i}', cat='Binary') for i in range(n)]
a = [pulp.LpVariable(f'a_{i}', cat='Binary') for i in range(n)]

# Função objetivo: minimizar a penalidade de b e a
model += pulp.lpSum([(Dmi[i] - DC) * b[i] * 2 + (DC - Dmi[i]) * a[i] for i in range(n)])

# Aplicação da técnica Big-M
for i in range(n):
    # Para b_i: b_i = 1 se Dmi > 1.05 * DC, caso contrário 0
    model += Dmi[i] - 1.05 * DC <= M * b[i], f"BigM_upper_b_{i}"
    model += Dmi[i] - 1.05 * DC >= -M * (1 - b[i]), f"BigM_lower_b_{i}"
    
    # Para a_i: a_i = 1 se Dmi <= DC, caso contrário 0
    model += DC - Dmi[i] <= M * a[i], f"BigM_upper_a_{i}"
    model += DC - Dmi[i] >= -M * (1 - a[i]), f"BigM_lower_a_{i}"

# Otimização
model.solve()

# Resultados
print(f"Status: {pulp.LpStatus[model.status]}")
print(f"Valor ótimo de DC: {DC.varValue}")
for i in range(n):
    print(f"b[{i}] = {b[i].varValue}, a[{i}] = {a[i].varValue}, Dmi[{i}] = {Dmi[i]}")
