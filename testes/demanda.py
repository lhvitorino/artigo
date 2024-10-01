import pulp as lp

# Vetor de demandas medidas (exemplo)
demandas_medidas = [55, 45, 60, 50, 70]  # kW medidos em cada período
T = len(demandas_medidas)  # Número de períodos

# Parâmetros do problema
custo_energia = 10  # Custo por kW consumido
penalidade_excesso = 20  # Penalidade por kW de excesso de demanda

# Criação do problema
prob = lp.LpProblem("Otimização_Demanda_Contratada", lp.LpMinimize)

# Variável de decisão: Demanda Contratada (contínua)
D_contratada = lp.LpVariable("Demanda_Contratada", lowBound=0)

# Variáveis de excesso para cada período
E = [lp.LpVariable(f"E_{t}", lowBound=0) for t in range(T)]  # Excesso de demanda em cada período

# Função objetivo: custo total (custo de energia + penalidade por excesso)
prob += (custo_energia * sum(demandas_medidas) + 
         penalidade_excesso * lp.lpSum(E)), "Custo_Total"

# Restrições: definir excesso de demanda para cada período
for t in range(T):
    prob += E[t] >= demandas_medidas[t] - D_contratada, f"Excesso_Demanda_{t}"

# Resolver o problema
prob.solve()

# Exibir os resultados
print("Status:", lp.LpStatus[prob.status])
print("Demanda Contratada Otimizada =", lp.value(D_contratada))
print("Custo Total =", lp.value(prob.objective))
for t in range(T):
    print(f"Período {t + 1}: Excesso = {lp.value(E[t])} kW")
