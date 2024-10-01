import pulp

# Dados
Dmi = [100, 200, 150, 300, 100, 200, 250, 100, 200, 300, 200, 100]
n = len(Dmi)
DC = pulp.LpVariable('DC', lowBound=0, cat='Integer')

# Criação do problema de minimização
prob = pulp.LpProblem("Minimizar Custo", pulp.LpMinimize)

# Variáveis binárias
a = [pulp.LpVariable(f'a_{i}', cat='Binary') for i in range(n)]
b = [pulp.LpVariable(f'b_{i}', cat='Binary') for i in range(n)]

# Variáveis auxiliares
z_b = [pulp.LpVariable(f'z_b_{i}', lowBound=0) for i in range(n)]
z_a = [pulp.LpVariable(f'z_a_{i}', lowBound=0) for i in range(n)]

# Função objetivo
prob += pulp.lpSum([z_b[i] + z_a[i] for i in range(n)])

# Restrições para variáveis binárias e auxiliares
M = 1000000  # Grande número

for i in range(n):
    # Linearização das condições para b:
    # Se Dmi >= 1.05 * DC, então b = 1, senão b = 0
    prob += Dmi[i] - 1.05 * DC >= -M * (1 - b[i])
    prob += Dmi[i] - 1.05 * DC <= M * b[i]
    
    # Linearização das condições para a:
    # Se Dmi < DC, então a = 1, senão a = 0
    prob += DC - Dmi[i] >= -M * (1 - a[i])
    prob += DC - Dmi[i] <= M * a[i]

    # Definir as variáveis auxiliares
    prob += z_b[i] <= (Dmi[i] - DC) * 2 + M * (1 - b[i])  # z_b = (Dmi - DC) * b
    prob += z_b[i] >= (Dmi[i] - DC) * 2 - M * (1 - b[i])
    prob += z_b[i] <= M * b[i]
    
    prob += z_a[i] <= (DC - Dmi[i]) + M * (1 - a[i])  # z_a = (DC - Dmi) * a
    prob += z_a[i] >= (DC - Dmi[i]) - M * (1 - a[i])
    prob += z_a[i] <= M * a[i]

# Resolver o problema
prob.solve()

# Ver resultados
print(f"Status: {pulp.LpStatus[prob.status]}")
print(f"Valor de DC: {pulp.value(DC)}")

for i in range(n):
    print(f"Mês {i+1}: a = {pulp.value(a[i])}, b = {pulp.value(b[i])}, z_b = {pulp.value(z_b[i])}, z_a = {pulp.value(z_a[i])}")
