import pulp

# Parâmetros de exemplo
Dmi = [100, 200]  # Demandas mensais
n = len(Dmi)
M = 10000  # Big-M (suficientemente grande)

# Criação do modelo
model = pulp.LpProblem("Minimize_costs", pulp.LpMinimize)

# Variável de decisão para DC (variável inteira)
DC = pulp.LpVariable('DC', lowBound=0, cat='Integer')

# Variáveis binárias b_i para ativar a penalidade se Dmi > 1.05 * DC
b = [pulp.LpVariable(f'b_{i}', cat='Binary') for i in range(n)]

# Variável de decisão para o excesso
excesso = [pulp.LpVariable(f'excesso_{i}', lowBound=0, cat='Integer') for i in range(n)]

# Função objetivo: minimizar a soma dos excessos
model += pulp.lpSum([excesso[i] for i in range(n)])

# Restrições para garantir que excesso = Dmi - DC quando Dmi > 1.05 * DC
for i in range(n):
    # Excesso deve ser igual a Dmi - DC quando b_i = 1
    model += excesso[i] <= (Dmi[i] - DC) + M * (1 - b[i]), f"Excesso_Upper_{i}"
    model += excesso[i] >= (Dmi[i] - DC) - M * (1 - b[i]), f"Excesso_Lower_{i}"
    
    # Quando b_i = 0, o excesso deve ser zero
    model += excesso[i] <= M * b[i], f"Excesso_Zero_{i}"

    # Big-M constraints for binary activation of b_i
    model += (Dmi[i] - 1.05 * DC) <= M * b[i], f"BigM_upper_{i}"
    model += (Dmi[i] - 1.05 * DC) >= -M * (1 - b[i]), f"BigM_lower_{i}"

# Otimização
model.solve()

# Resultados
print(f"Status: {pulp.LpStatus[model.status]}")
print(f"Valor ótimo de DC: {DC.varValue}")
for i in range(n):
    print(f"b[{i}] = {b[i].varValue}, Dmi[{i}] = {Dmi[i]}, Excesso[{i}] = {excesso[i].varValue}")

