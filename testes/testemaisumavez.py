import pulp

# Define o problema como um problema de minimização
model = pulp.LpProblem("Minimize_DC_Problem", pulp.LpMinimize)

# Definir as variáveis de decisão
b = pulp.LpVariable.dicts("b", range(12), 0, 1, pulp.LpBinary)
a = pulp.LpVariable.dicts("a", range(12), 0, 1, pulp.LpBinary)
DC = pulp.LpVariable("DC", lowBound=1, cat='Integer')  # DC deve ser um número inteiro positivo

# Exemplo de valores de Dm
Dm = [100, 102, 98, 105, 110, 95, 103, 108, 97, 106, 104, 99]  # Substitua pelos valores reais de Dm
M = 10000  # Constante Big-M

# Função objetivo: Minimizar a soma da expressão dada
model += pulp.lpSum([(Dm[i] - DC) * 2 * b[i] + (DC - Dm[i]) * a[i] for i in range(12)])

# Restrições Big-M para b_i com base em Dm_i e DC
for i in range(12):
    # Se Dm_i >= 1.05 * DC, então b_i = 1, caso contrário b_i = 0
    model += Dm[i] - 1.05 * DC <= M * (1 - b[i])  # Garante que b_i = 1 se Dm_i >= 1.05 * DC
    model += Dm[i] - 1.05 * DC >= -M * b[i]       # Garante que b_i = 0 se Dm_i < 1.05 * DC

# Restrições Big-M para a_i com base em Dm_i e DC
for i in range(12):
    # Se Dm_i < DC, então a_i = 1, caso contrário a_i = 0
    model += DC - Dm[i] > M * (1 - a[i])  # Garante que a_i = 1 se Dm_i < DC
    model += DC - Dm[i] <= M * a[i]       # Garante que a_i = 0 se Dm_i >= DC

# Resolver o modelo
model.solve()

# Imprimir os resultados
print(f"Status: {pulp.LpStatus[model.status]}")
print(f"Valor ótimo de DC: {pulp.value(DC)}")
for i in range(12):
    print(f"b[{i}] = {pulp.value(b[i])}, a[{i}] = {pulp.value(a[i])}")
