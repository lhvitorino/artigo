import pulp

# Dados
dMi = [3542.40, 4285.44, 5175.36, 5356.80, 4596.48, 3214.08, 3196.80, 2946.24, 2730.24, 2868.48, 3715.20, 3723.84]
n = len(dMi)
Tc = 22.16
Ts = 18.40

# Variáveis de decisão
dC1 = pulp.LpVariable('dC1', lowBound=0, upBound=4800, cat='Integer')
dC2 = pulp.LpVariable('dC2', lowBound=30, upBound=4800, cat='Integer')
# dC3 = pulp.LpVariable('dC3', lowBound=0, upBound=4800, cat='Integer')
# dC4 = pulp.LpVariable('dC4', lowBound=0, upBound=4800, cat='Integer')

# Criação do problema de minimização
prob = pulp.LpProblem("Minimizar Custo", pulp.LpMinimize)

# Variáveis binárias
bsub = [pulp.LpVariable(f'bsub_{i}', cat='Binary') for i in range(n)]
bsob = [pulp.LpVariable(f'bsob_{i}', cat='Binary') for i in range(n)]
bsut = [pulp.LpVariable(f'bsut_{i}', cat='Binary') for i in range(n)]
bsot = [pulp.LpVariable(f'bsot_{i}', cat='Binary') for i in range(n)]


# Variáveis auxiliares
z_sub = [pulp.LpVariable(f'z_sub_{i}', lowBound=0) for i in range(n)]
z_sob = [pulp.LpVariable(f'z_sob_{i}', lowBound=0) for i in range(n)]
z_sut = [pulp.LpVariable(f'z_sut_{i}', lowBound=0) for i in range(n)]
z_sot = [pulp.LpVariable(f'z_sot_{i}', lowBound=0) for i in range(n)]

# Função objetivo
prob += pulp.lpSum([(z_sub[i] * 2 * Tc) + (z_sob[i] * Ts) + (z_sut[i] * 2 * Tc) + (z_sot[i] * Ts) for i in range(n)])

# Restrições de acréscimo e decréscimos de demanda

prob += dC1 >= 1.05 * dC2 # Segundo período deve subir 5% em relação ao primeiro para configurar período de teste
# prob += dC2 >= 30 # demanda minima contratada na redução deve ser maior que 30kW
# prob += dC3 >= 1.05 * dC2 # Quarto período deve subir 5% em relação ao terceiro para configurar período de teste

# Restrições para variáveis binárias e auxiliares
M = 1000000  # Constante Big-M

for i in range(n):
    if i >= 0 and i <= 5:
        # Linearização das condições para bsub:
        # Se dMi >= 1.05 * dC1, então bsub = 1, senão bsub = 0
        prob += dMi[i] - 1.05 * dC1 >= -M * (1 - bsub[i])
        prob += dMi[i] - 1.05 * dC1 <= M * bsub[i]
    
        # Linearização das condições para bsob:
        # Se dmi < dC3, então bsob = 1, senão bsob = 0
        prob += dC1 - dMi[i] >= -M * (1 - bsob[i])
        prob += dC1 - dMi[i] <= M * bsob[i]

        # Definir as variáveis auxiliares
        prob += z_sub[i] <= (dMi[i] - dC1) + M * (1 - bsub[i])  # z_sub = (dMi - dC1) * 2 * Tc * bsub
        prob += z_sub[i] >= (dMi[i] - dC1) - M * (1 - bsub[i])
        prob += z_sub[i] <= M * bsub[i]
    
        prob += z_sob[i] <= (dC1 - dMi[i]) + M * (1 - bsob[i])  # z_sob = (dC1 - dMi) * Ts * bsob
        prob += z_sob[i] >= (dC1 - dMi[i]) - M * (1 - bsob[i])
        prob += z_sob[i] <= M * bsob[i]

    if i >= 6 and i <= 11:
        # Linearização das condições para bsub:
        # Se dMi >= 1.05 * dC2, então bsub = 1, senão bsub = 0
        prob += dMi[i] - 1.05 * dC2 >= -M * (1 - bsub[i])
        prob += dMi[i] - 1.05 * dC2 <= M * bsub[i]
    
        # Linearização das condições para bsob:
        # Se dMi < dC3, então bsob = 1, senão bsob = 0
        prob += dC2 - dMi[i] >= -M * (1 - bsob[i])
        prob += dC2 - dMi[i] <= M * bsob[i]

        # Definir as variáveis auxiliares
        prob += z_sub[i] <= (dMi[i] - dC2) + M * (1 - bsub[i])  # z_sub = (dMi - dC2) * 2 * Tc * bsub
        prob += z_sub[i] >= (dMi[i] - dC2) - M * (1 - bsub[i])
        prob += z_sub[i] <= M * bsub[i]
    
        prob += z_sob[i] <= (dC2 - dMi[i]) + M * (1 - bsob[i])  # z_sob = (dC2 - dMi) * Ts * bsob
        prob += z_sob[i] >= (dC2 - dMi[i]) - M * (1 - bsob[i])
        prob += z_sob[i] <= M * bsob[i]
    
    
# Resolver o problema
prob.solve()

# Ver resultados
print(f"Status: {pulp.LpStatus[prob.status]}")
print(f"Valor de dC1: {pulp.value(dC1)}")
print(f"Valor de dC2: {pulp.value(dC2)}")
# print(f"Valor de dC3: {pulp.value(dC3)}")
# print(f"Valor de dC4: {pulp.value(dC4)}")

for i in range(n):
    print(f"Mês {i+1}: bsub = {pulp.value(bsub[i])}, bsob = {pulp.value(bsob[i])}, bsut = {pulp.value(bsut[i])}, bsot = {pulp.value(bsot[i])}")
    print(f"Mês {i+1}: z_sub = {pulp.value(z_sub[i])}, z_sob = {pulp.value(z_sob[i])}, z_sut = {pulp.value(z_sut[i])}, z_sot = {pulp.value(z_sot[i])}")
