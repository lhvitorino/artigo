import pulp as lp

# Dados do problema
demanda_medida = [45, 48, 52, 58, 60]  # Demanda medida em cada período (kW)
c_icms = 0.30  # Tarifa com ICMS (R$/kW)
c_sem_icms = 0.25  # Tarifa sem ICMS (R$/kW)

# Criação do problema de minimização
prob = lp.LpProblem("Otimização_Demanda_Contratada", lp.LpMinimize)

# Variável de decisão: Demanda contratada
D_contratada = lp.LpVariable("D_contratada", lowBound=0)

# Variáveis de penalidade para cada período
penalidades = []

# Função objetivo: calcular as penalidades
for t, D_t in enumerate(demanda_medida):
    excesso = lp.LpVariable(f"Excesso_{t}", lowBound=0)
    falta = lp.LpVariable(f"Falta_{t}", lowBound=0)
    
    # Regra 1: Penalidade por excesso de 5% acima da demanda contratada
    prob += excesso >= D_t - 1.05 * D_contratada, f"Excesso_Regra_{t}"
    
    # Regra 2: Penalidade por demanda abaixo da contratada
    prob += falta >= D_contratada - D_t, f"Falta_Regra_{t}"
    
    # Penalidade total no período t
    penalidade = 2 * c_icms * excesso + c_sem_icms * falta
    penalidades.append(penalidade)

# Função objetivo: somar as penalidades de todos os períodos
prob += lp.lpSum(penalidades), "Custo Total"

# Resolução do problema
prob.solve()

# Resultado
print("Status:", lp.LpStatus[prob.status])
print("Demanda Contratada Ótima:", lp.value(D_contratada), "kW")
for t, D_t in enumerate(demanda_medida):
    print(f"Período {t + 1}: Demanda Medida = {D_t} kW, Excesso = {lp.value(prob.variablesDict()[f'Excesso_{t}'])} kW, Falta = {lp.value(prob.variablesDict()[f'Falta_{t}'])} kW")
print("Custo Total =", lp.value(prob.objective), "R$")
