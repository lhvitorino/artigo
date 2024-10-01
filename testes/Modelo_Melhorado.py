import pulp

# Definir o modelo de otimização (minimização)
model = pulp.LpProblem("Minimize Energy Demand", pulp.LpMinimize)

# Definir os parâmetros (Dmi para cada mês i)
Dmi = [100, 200]  # Exemplo de demanda para 12 meses
n = len(Dmi)
M = 10000 # constante big M

# Variáveis de decisão
DC = pulp.LpVariable('DC', lowBound=0, upBound=1, cat='Integer')  # DC deve ser inteiro
a = [pulp.LpVariable(f'a_{i}', cat='Binary') for i in range(n)]
b = [pulp.LpVariable(f'b_{i}', cat='Binary') for i in range(n)]

# Variável para o excesso
excesso = [pulp.LpVariable(f'excesso_{i}', lowBound=0, cat='Integer') for i in range(n)]
falta = [pulp.LpVariable(f'falta_{i}', lowBound=0, cat='Integer') for i in range(n)]

# Função objetivo
model += pulp.lpSum([excesso[i] * 2 + falta[i] for i in range(n)])

# Restrições para as variáveis binárias b_i e a_i
for i in range(n):
    # Excesso deve ser igual a Dmi - DC quando b_i = 1
    model += excesso[i] <= (Dmi[i] - DC) + M * (1 - b[i]), f"Excesso_Upper_{i}"
    model += excesso[i] >= (Dmi[i] - DC) - M * (1 - b[i]), f"Excesso_Lower_{i}"

    # Quando b_i = 0, o excesso deve ser zero
    model += excesso[i] <= M * b[i], f"Excesso_Zero_{i}"

    # Big-M constraints for binary activation of b_i
    model += (Dmi[i] - 1.05 * DC) <= M * b[i], f"BigM_upper_Excesso{i}"
    model += (Dmi[i] - 1.05 * DC) >= -M * (1 - b[i]), f"BigM_lower_Excesso{i}"

    # Falta deve ser igual a DC - Dmi quando a_i = 1
    model += falta[i] <= (DC - Dmi[i]) + M * (1 - a[i]), f"Falta_Upper_{i}"
    model += falta[i] >= (DC - Dmi[i]) - M * (1 - a[i]), f"Falta_Lower_{i}"

    # Quando b_i = 0, o excesso deve ser zero
    model += falta[i] <= M * a[i], f"Falta_Zero_{i}"

    # Big-M constraints for binary activation of a_i
    model += (Dmi[i] - DC) >= M * a[i], f"BigM_upper_Falta{i}"
    model += (Dmi[i] - DC) <= -M * (1 - a[i]), f"BigM_lower_Falta{i}"


# Resolver o modelo
model.solve()

# Exibir resultados
print("Status:", pulp.LpStatus[model.status])
print(f"Valor de DC: {DC.varValue}")
for i in range(n):
    print(f"a_{i}: {a[i].varValue}, b_{i}: {b[i].varValue}, Excesso[{i}] = {excesso[i].varValue}, falta[{i}] = {falta[i].varValue}")
