import pulp as lp

# Parâmetros do problema
T = 5  # Número de períodos
demanda_contratada = 50  # Demanda contratada (kW)
custo_energia = 10  # Custo por kW consumido
penalidade_excesso = 20  # Penalidade por kW de excesso de demanda

# Criação do problema
prob = lp.LpProblem("Minimização_Custo_Energia", lp.LpMinimize)

# Variáveis de decisão
D = [lp.LpVariable(f"D_{t}", lowBound=0) for t in range(T)]  # Demanda em cada período
E = [lp.LpVariable(f"E_{t}", lowBound=0) for t in range(T)]  # Excesso de demanda

# Função objetivo: custo da energia consumida + penalidade pelo excesso
prob += lp.lpSum([custo_energia * D[t] + penalidade_excesso * E[t] for t in range(T)]), "Custo Total"

# Restrições
for t in range(T):
    prob += E[t] >= D[t] - demanda_contratada, f"Excesso_Demanda_{t}"
    prob += E[t] >= 0, f"Excesso_Positive_{t}"  # Garantir que o excesso é não negativo

# Resolução
prob.solve()

# Resultados
print("Status:", lp.LpStatus[prob.status])
for t in range(T):
    print(f"Período {t + 1}: Demanda = {lp.value(D[t])} kW, Excesso = {lp.value(E[t])} kW")
print("Custo Total =", lp.value(prob.objective))
