import pulp as lp
from pulp import LpInteger

# Dados do problema
demanda_medida = [3482, 2238, 2704, 3542, 3024, 2627, 2160, 1676, 2307, 2877, 2566, 3154]  # Demanda medida em cada período no ano 2023 - CMD01(kW)
c_icms = 22.16  # Tarifa com ICMS (R$/kW)
c_sem_icms = 18.40  # Tarifa sem ICMS (R$/kW)

# Criação do problema de minimização
prob = lp.LpProblem("Otimização_Demanda_Contratada", lp.LpMinimize)

# Variável de decisão: Demanda contratada
dC_1 = lp.LpVariable("dC_1", lowBound=0, upBound=None, cat=LpInteger)
dC_2 = lp.LpVariable("dC_2", lowBound=0, upBound=None, cat=LpInteger)
dC_3 = lp.LpVariable("dC_2", lowBound=0, upBound=None, cat=LpInteger)
dC_4 = lp.LpVariable("dC_2", lowBound=0, upBound=None, cat=LpInteger)

# Variáveis de penalidade para cada período
penalidades = []

# Função objetivo: calcular as penalidades
for i, dM_i in enumerate(demanda_medida):
    excesso = lp.LpVariable(f"Excesso_{i}", lowBound=0)
    falta = lp.LpVariable(f"Falta_{i}", lowBound=0)
    if i >= 0 and i <= 2: # Janeiro - Marco com dC_1
        # Regra 1: Penalidade por excesso de 5% acima da demanda contratada
        prob += excesso >= dM_i - 1.05 * dC_1, f"Excesso_Regra_{i}"
        # Regra 2: Penalidade por demanda abaixo da contratada
        prob += falta >= dC_1 - dM_i, f"Falta_Regra_{i}"
    if i >= 3 and i <= 5: # Abril - Junho com dC_2 > 1.05 * dC_1 e no Período de Testes
        # Regra 1: Penalidade por excesso de 5% acima da demanda contratada janeiro-junho
        prob += excesso >= dM_i - 1.05 * dC_2, f"Excesso_Regra_{i}"
        # Regra 2: Penalidade por demanda abaixo da contratada - Como é Período de Testes, usa a penalidade antes da mudança (dC_1)
        prob += falta >= dC_1 - dM_i, f"Falta_Regra_{i}"
    if i >= 6 and i <= 8: # Julho - Setembro com dC_3 < dc_2
        # Regra 1: Penalidade por excesso de 5% acima da demanda contratada janeiro-junho
        prob += excesso >= dM_i - 1.05 * dC_3, f"Excesso_Regra_{i}"
        # Regra 2: Penalidade por demanda abaixo da contratada
        prob += falta >= dC_3 - dM_i, f"Falta_Regra_{i}"
    if i <= 9 and i <= 11: # Outubro - Dezembro com dC_4
        # Regra 1: Penalidade por excesso de 5% acima da demanda contratada janeiro-junho
        prob += excesso >= dM_i - 1.05 * dC_4, f"Excesso_Regra_{i}"
        # Regra 2: Penalidade por demanda abaixo da contratada
        prob += falta >= dC_3 - dM_i, f"Falta_Regra_{i}"
    # Penalidade total no período t
    penalidade = 2 * c_icms * excesso + c_sem_icms * falta
    penalidades.append(penalidade)

# Função objetivo: somar as penalidades de todos os períodos
prob += lp.lpSum(penalidades), "Custo Total"

# Resolução do problema
prob.solve()

# Resultado
print("Status:", lp.LpStatus[prob.status])
print("Demanda Contratada 1:", lp.value(dC_1), "kW")
print("Demanda Contratada 2:", lp.value(dC_2), "kW")
print("Demanda Contratada 3:", lp.value(dC_3), "kW")
print("Demanda Contratada 4:", lp.value(dC_4), "kW")
for t, dM_i in enumerate(demanda_medida):
    print(f"Período {t + 1}: Demanda Medida = {dM_i} kW, Excesso = {lp.value(prob.variablesDict()[f'Excesso_{t}'])} kW, Falta = {lp.value(prob.variablesDict()[f'Falta_{t}'])} kW")
print("Custo Total =", lp.value(prob.objective), "R$")
