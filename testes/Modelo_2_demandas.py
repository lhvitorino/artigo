import pulp as lp
from pulp import LpInteger

# Dados do problema
demanda_medida = [3482, 2238, 2704, 3542, 3024, 2627, 2160, 1676, 2307, 2877, 2566, 3154]  # Demanda medida em cada período no ano 2023 - CMD01(kW)
c_icms = 22.16  # Tarifa com ICMS (R$/kW)
c_sem_icms = 18.40  # Tarifa sem ICMS (R$/kW)

# Criação do problema de minimização
prob = lp.LpProblem("Otimização_Demanda_Contratada", lp.LpMinimize)

# Variável de decisão: Demanda contratada
D_contratada_inicial = lp.LpVariable("D_contratada_inicial", lowBound=0, upBound=None, cat=LpInteger)
D_contratada_final = lp.LpVariable("D_contratada_final", lowBound=0, upBound=None, cat=LpInteger)

# Variáveis de penalidade para cada período
penalidades = []

# Função objetivo: calcular as penalidades
for t, D_t in enumerate(demanda_medida):
    excesso = lp.LpVariable(f"Excesso_{t}", lowBound=0)
    falta = lp.LpVariable(f"Falta_{t}", lowBound=0)
    
    if t <= 6:
        # Regra 1: Penalidade por excesso de 5% acima da demanda contratada janeiro-junho
        prob += excesso >= D_t - 1.05 * D_contratada_inicial, f"Excesso_Regra_{t}"
        # Regra 2: Penalidade por demanda abaixo da contratada
        prob += falta >= D_contratada_inicial - D_t, f"Falta_Regra_{t}"
    else:
        # Regra 1: Penalidade por excesso de 5% acima da demanda contratada janeiro-junho
        prob += excesso >= D_t - 1.05 * D_contratada_final, f"Excesso_Regra_{t}"
        # Regra 2: Penalidade por demanda abaixo da contratada
        prob += falta >= D_contratada_final - D_t, f"Falta_Regra_{t}"
    # Penalidade total no período t
    penalidade = 2 * c_icms * excesso + c_sem_icms * falta
    penalidades.append(penalidade)

# Função objetivo: somar as penalidades de todos os períodos
prob += lp.lpSum(penalidades), "Custo Total"

# Resolução do problema
prob.solve()

# Resultado
print("Status:", lp.LpStatus[prob.status])
print("Demanda Contratada Ótima Inicial:", lp.value(D_contratada_inicial), "kW")
print("Demanda Contratada Ótima Final:", lp.value(D_contratada_final), "kW")
for t, D_t in enumerate(demanda_medida):
    print(f"Período {t + 1}: Demanda Medida = {D_t} kW, Excesso = {lp.value(prob.variablesDict()[f'Excesso_{t}'])} kW, Falta = {lp.value(prob.variablesDict()[f'Falta_{t}'])} kW")
print("Custo Total =", lp.value(prob.objective), "R$")
