import pulp

# Dados
Dmi = [100, 200]
n = len(Dmi)
DC = pulp.LpVariable('DC', lowBound=0, cat='Integer')

# Criação do problema de minimização
prob = pulp.LpProblem("Minimizar Custo", pulp.LpMinimize)

# Variáveis binárias
a = [pulp.LpVariable(f'a_{i}', cat='Binary') for i in range(n)]
b = [pulp.LpVariable(f'b_{i}', cat='Binary') for i in range(n)]

# Função objetivo
prob += pulp.lpSum([(Dmi[i] - DC) * (2 * b[i]) + (DC - Dmi[i]) * a[i] for i in range(n)])

# Restrições para variáveis binárias
for i in range(n):
    # Linearização das condições para b:
    # Se Dmi >= 1.05 * DC, então b = 1, senão b = 0
    prob += Dmi[i] - 1.05 * DC >= -1000000 * (1 - b[i])  # grande número M para linearização
    prob += Dmi[i] - 1.05 * DC <= 1000000 * b[i]
    
    # Linearização das condições para a:
    # Se Dmi < DC, então a = 1, senão a = 0
    prob += DC - Dmi[i] >= -1000000 * (1 - a[i])  # grande número M para linearização
    prob += DC - Dmi[i] <= 1000000 * a[i]

# Resolver o problema
prob.solve()

# Ver resultados
print(f"Status: {pulp.LpStatus[prob.status]}")
print(f"Valor de DC: {pulp.value(DC)}")

for i in range(n):
    print(f"Mês {i+1}: a = {pulp.value(a[i])}, b = {pulp.value(b[i])}")
